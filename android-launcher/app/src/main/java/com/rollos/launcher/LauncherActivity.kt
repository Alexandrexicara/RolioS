package com.rollos.launcher

import android.app.Activity
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.FrameLayout
import android.widget.GridLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/** Roll iOS: iPhone-inspired home screen with Android package discovery. */
class LauncherActivity : Activity() {
    private lateinit var appGrid: GridLayout
    private val packageChanges = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) = renderApps()
    }
    private var receiverRegistered = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = Color.rgb(30, 54, 103)
        window.navigationBarColor = Color.rgb(25, 42, 82)
        if (Build.VERSION.SDK_INT >= 29) {
            window.isNavigationBarContrastEnforced = false
            window.isStatusBarContrastEnforced = false
        }

        val wallpaper = GradientDrawable(
            GradientDrawable.Orientation.TL_BR,
            intArrayOf(Color.rgb(74, 111, 190), Color.rgb(83, 75, 151), Color.rgb(30, 43, 91))
        )
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(20), dp(18), dp(20), dp(14))
            background = wallpaper
        }

        val status = TextView(this).apply {
            text = SimpleDateFormat("HH:mm", Locale("pt", "BR")).format(Date()) +
                "                                      ●  ●  ▰"
            textSize = 13f
            setTypeface(null, Typeface.BOLD)
            setTextColor(Color.WHITE)
        }
        root.addView(status, LinearLayout.LayoutParams(-1, dp(24)))

        val date = TextView(this).apply {
            text = SimpleDateFormat("EEEE, d 'de' MMMM", Locale("pt", "BR"))
                .format(Date()).replaceFirstChar { it.uppercase(Locale("pt", "BR")) }
            textSize = 15f
            gravity = Gravity.CENTER
            setTextColor(Color.WHITE)
            setPadding(0, dp(18), 0, dp(4))
        }
        root.addView(date)

        val clock = TextView(this).apply {
            text = SimpleDateFormat("HH:mm", Locale("pt", "BR")).format(Date())
            textSize = 48f
            gravity = Gravity.CENTER
            setTypeface(Typeface.create("sans-serif-light", Typeface.NORMAL))
            setTextColor(Color.WHITE)
            setPadding(0, 0, 0, dp(18))
        }
        root.addView(clock)

        appGrid = GridLayout(this).apply {
            columnCount = 4
            useDefaultMargins = false
            alignmentMode = GridLayout.ALIGN_BOUNDS
        }
        root.addView(appGrid, LinearLayout.LayoutParams(-1, 0, 1f))

        val pageDots = TextView(this).apply {
            text = "●  ○  ○"
            textSize = 10f
            gravity = Gravity.CENTER
            setTextColor(Color.WHITE)
            setPadding(0, dp(5), 0, dp(12))
        }
        root.addView(pageDots)

        val dock = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(dp(8), dp(8), dp(8), dp(8))
            background = rounded(Color.argb(65, 245, 247, 255), dp(25))
        }
        root.addView(dock, LinearLayout.LayoutParams(-1, dp(78)))
        setContentView(root)
        renderApps(dock)
    }

    override fun onResume() {
        super.onResume()
        renderApps()
        if (!receiverRegistered) {
            val filter = IntentFilter().apply {
                addAction(Intent.ACTION_PACKAGE_ADDED)
                addAction(Intent.ACTION_PACKAGE_REMOVED)
                addAction(Intent.ACTION_PACKAGE_CHANGED)
                addDataScheme("package")
            }
            if (Build.VERSION.SDK_INT >= 33) {
                registerReceiver(packageChanges, filter, Context.RECEIVER_NOT_EXPORTED)
            } else {
                @Suppress("DEPRECATION")
                registerReceiver(packageChanges, filter)
            }
            receiverRegistered = true
        }
    }

    override fun onPause() {
        if (receiverRegistered) {
            try { unregisterReceiver(packageChanges) } catch (_: IllegalArgumentException) { }
            receiverRegistered = false
        }
        super.onPause()
    }

    @Suppress("DEPRECATION")
    private fun renderApps(dock: LinearLayout? = null) {
        if (!::appGrid.isInitialized) return
        appGrid.removeAllViews()
        dock?.removeAllViews()

        val apps = packageManager.queryIntentActivities(
            Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER),
            PackageManager.MATCH_ALL
        ).distinctBy { it.activityInfo.packageName }
            .sortedBy { it.loadLabel(packageManager).toString().lowercase(Locale.getDefault()) }

        apps.forEachIndexed { index, info ->
            val openApp = View.OnClickListener {
                packageManager.getLaunchIntentForPackage(info.activityInfo.packageName)?.let(::startActivity)
            }
            val item = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                gravity = Gravity.CENTER
                setPadding(dp(3), dp(7), dp(3), dp(9))
                isClickable = true
                isFocusable = true
                setOnClickListener(openApp)
            }
            val iconFrame = FrameLayout(this).apply {
                background = rounded(Color.argb(35, 255, 255, 255), dp(15))
                clipToOutline = true
            }
            iconFrame.addView(ImageView(this).apply {
                setImageDrawable(info.loadIcon(packageManager))
                scaleType = ImageView.ScaleType.FIT_CENTER
                contentDescription = info.loadLabel(packageManager).toString()
                setPadding(dp(2), dp(2), dp(2), dp(2))
            }, FrameLayout.LayoutParams(dp(58), dp(58), Gravity.CENTER))
            item.addView(iconFrame, LinearLayout.LayoutParams(dp(62), dp(62)))
            item.addView(TextView(this).apply {
                text = info.loadLabel(packageManager)
                textSize = 11f
                gravity = Gravity.CENTER
                maxLines = 2
                setTextColor(Color.WHITE)
                setShadowLayer(2f, 0f, 1f, Color.BLACK)
                setPadding(0, dp(5), 0, 0)
            }, LinearLayout.LayoutParams(-1, dp(34)))

            appGrid.addView(item, GridLayout.LayoutParams(
                GridLayout.spec(index / 4, 1f), GridLayout.spec(index % 4, 1f)
            ).apply { width = 0; height = dp(104) })

            if (index < 4 && dock != null) {
                val dockIcon = ImageView(this).apply {
                    setImageDrawable(info.loadIcon(packageManager))
                    scaleType = ImageView.ScaleType.FIT_CENTER
                    contentDescription = info.loadLabel(packageManager).toString()
                    isClickable = true
                    setOnClickListener(openApp)
                }
                dock.addView(dockIcon, LinearLayout.LayoutParams(0, dp(58), 1f).apply {
                    marginStart = dp(5)
                    marginEnd = dp(5)
                })
            }
        }
    }

    private fun rounded(color: Int, radius: Int) = GradientDrawable().apply {
        setColor(color)
        cornerRadius = radius.toFloat()
    }

    private fun dp(value: Int) = (value * resources.displayMetrics.density).toInt()
}
