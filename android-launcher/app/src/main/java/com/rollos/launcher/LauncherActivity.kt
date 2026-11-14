package com.rollos.launcher

import android.app.Activity
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.view.Gravity
import android.widget.GridLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/** Native RollOS home screen. Android PackageManager is the source of truth. */
class LauncherActivity : Activity() {
    private lateinit var appGrid: GridLayout
    private val packageChanges = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) = renderApps()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = Color.rgb(7, 19, 29)
        window.navigationBarColor = Color.rgb(7, 19, 29)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(20), dp(26), dp(20), dp(16))
            setBackgroundColor(Color.rgb(7, 19, 29))
        }
        root.addView(TextView(this).apply {
            text = "RollOS  •  Tela inicial"
            textSize = 13f
            setTextColor(Color.rgb(171, 211, 218))
        })
        root.addView(TextView(this).apply {
            text = SimpleDateFormat("HH:mm", Locale("pt", "BR")).format(Date())
            textSize = 54f
            gravity = Gravity.CENTER
            setTextColor(Color.WHITE)
            setPadding(0, dp(38), 0, dp(4))
        })
        root.addView(TextView(this).apply {
            text = SimpleDateFormat("EEEE, d 'de' MMMM", Locale("pt", "BR")).format(Date())
            textSize = 14f
            gravity = Gravity.CENTER
            setTextColor(Color.LTGRAY)
            setPadding(0, 0, 0, dp(28))
        })
        root.addView(TextView(this).apply {
            text = "SEUS APLICATIVOS"
            textSize = 12f
            letterSpacing = .12f
            setTextColor(Color.rgb(121, 234, 213))
            setPadding(0, 0, 0, dp(14))
        })
        appGrid = GridLayout(this).apply { columnCount = 4 }
        root.addView(appGrid, LinearLayout.LayoutParams(-1, 0, 1f))
        root.addView(TextView(this).apply {
            text = "Os aplicativos instalados com ícone de inicialização aparecem aqui automaticamente."
            textSize = 11f
            gravity = Gravity.CENTER
            setTextColor(Color.rgb(139, 166, 178))
            setPadding(0, dp(12), 0, dp(8))
        })
        setContentView(root)
        renderApps()
    }

    override fun onResume() {
        super.onResume()
        renderApps()
        val filter = IntentFilter().apply {
            addAction(Intent.ACTION_PACKAGE_ADDED)
            addAction(Intent.ACTION_PACKAGE_REMOVED)
            addAction(Intent.ACTION_PACKAGE_CHANGED)
            addDataScheme("package")
        }
        if (Build.VERSION.SDK_INT >= 33) registerReceiver(packageChanges, filter, Context.RECEIVER_NOT_EXPORTED)
        else @Suppress("DEPRECATION") registerReceiver(packageChanges, filter)
    }

    override fun onPause() {
        try { unregisterReceiver(packageChanges) } catch (_: IllegalArgumentException) { }
        super.onPause()
    }

    @Suppress("DEPRECATION")
    private fun renderApps() {
        if (!::appGrid.isInitialized) return
        appGrid.removeAllViews()
        val apps = packageManager.queryIntentActivities(
            Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER),
            PackageManager.MATCH_ALL
        ).distinctBy { it.activityInfo.packageName }
            .sortedBy { it.loadLabel(packageManager).toString().lowercase(Locale.getDefault()) }
        apps.forEachIndexed { index, info ->
            val item = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                gravity = Gravity.CENTER
                setPadding(dp(3), dp(8), dp(3), dp(12))
                isClickable = true
                isFocusable = true
                setOnClickListener {
                    packageManager.getLaunchIntentForPackage(info.activityInfo.packageName)?.let(::startActivity)
                }
            }
            item.addView(ImageView(this).apply {
                setImageDrawable(info.loadIcon(packageManager))
                scaleType = ImageView.ScaleType.FIT_CENTER
                contentDescription = info.loadLabel(packageManager).toString()
            }, LinearLayout.LayoutParams(dp(50), dp(50)))
            item.addView(TextView(this).apply {
                text = info.loadLabel(packageManager)
                textSize = 11f
                gravity = Gravity.CENTER
                maxLines = 2
                setTextColor(Color.WHITE)
                setPadding(0, dp(7), 0, 0)
            }, LinearLayout.LayoutParams(-1, -2))
            appGrid.addView(item, GridLayout.LayoutParams(
                GridLayout.spec(index / 4, 1f), GridLayout.spec(index % 4, 1f)
            ).apply { width = 0; height = dp(96) })
        }
    }

    private fun dp(value: Int) = (value * resources.displayMetrics.density).toInt()
}
