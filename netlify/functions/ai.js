const MODEL = process.env.NVIDIA_MODEL || "nvidia/nemotron-3.5-bolt-e4b";
const BASE_URL = (process.env.NVIDIA_BASE_URL || "https://integrate.api.nvidia.com/v1").replace(/\/$/, "");
const WINDOW_MS = 60_000;
const MAX_REQUESTS = 20;
const requestLog = new Map();

function json(statusCode, payload) {
  return {
    statusCode,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff"
    },
    body: JSON.stringify(payload)
  };
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return json(405, { error: "Método não permitido." });
  }

  const apiKey = process.env.NVIDIA_API_KEY;
  if (!apiKey) {
    return json(503, {
      error: "O serviço NVIDIA ainda não foi configurado. O administrador precisa cadastrar NVIDIA_API_KEY no Netlify."
    });
  }

  let body;
  try {
    body = JSON.parse(event.body || "{}");
  } catch {
    return json(400, { error: "Corpo da solicitação inválido." });
  }

  const message = typeof body.message === "string" ? body.message.trim() : "";
  if (!message || message.length > 6000) {
    return json(400, { error: "Envie uma mensagem de até 6.000 caracteres." });
  }

  const ip = event.headers["x-nf-client-connection-ip"] || event.headers["client-ip"] || "unknown";
  const now = Date.now();
  const recent = (requestLog.get(ip) || []).filter((time) => now - time < WINDOW_MS);
  if (recent.length >= MAX_REQUESTS) {
    return json(429, { error: "Muitas mensagens em pouco tempo. Aguarde um minuto." });
  }
  recent.push(now);
  requestLog.set(ip, recent);

  try {
    const upstream = await fetch(`${BASE_URL}/chat/completions`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: MODEL,
        messages: [
          {
            role: "system",
            content: "Você é Jarvis, o assistente de inteligência artificial do RollOS. Fale em português brasileiro, com clareza, educação e objetividade. Ajude com tarefas e explique limites reais. Nunca diga que controlou hardware, arquivos, contas ou serviços sem uma ferramenta autorizada que confirme a ação."
          },
          { role: "user", content: message }
        ],
        temperature: 0.3,
        max_tokens: 1200
      }),
      signal: AbortSignal.timeout(60_000)
    });

    const result = await upstream.json().catch(() => ({}));
    if (!upstream.ok) {
      const detail = result.error?.message || result.message || `HTTP ${upstream.status}`;
      return json(502, { error: `A NVIDIA não concluiu a resposta: ${String(detail).slice(0, 300)}` });
    }

    const reply = result.choices?.[0]?.message?.content;
    if (typeof reply !== "string" || !reply.trim()) {
      return json(502, { error: "A NVIDIA retornou uma resposta vazia ou em formato inesperado." });
    }
    return json(200, { reply: reply.trim(), model: MODEL });
  } catch (error) {
    const message = error.name === "TimeoutError"
      ? "A NVIDIA demorou para responder. Tente novamente."
      : "Não foi possível conectar ao serviço NVIDIA.";
    return json(502, { error: message });
  }
};
