package com.ringga.mapbox

import android.Manifest
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.mapbox.android.core.location.*
import com.ringga.mapbox.databinding.ActivityMainBinding
import com.ringga.mapbox.service.BackgrounLocationService
import com.ringga.mapbox.service.BackgrounLocationService.Companion.locationListeners


class MainActivity : AppCompatActivity() {
    private var broadcastReceiver: BroadcastReceiver? = null
    var cnt = 0
    private lateinit var binding: ActivityMainBinding
    override fun onResume() {
        super.onResume()

    }

    override fun onDestroy() {
        super.onDestroy()
        if (broadcastReceiver != null) {
            unregisterReceiver(broadcastReceiver)
        }
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
//        Mapbox.getInstance(this, getString(R.string.mapbox_access_token))
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        if (!runtime_permissions())
            enable_buttons();

    }

    private fun runtime_permissions(): Boolean {
        if (Build.VERSION.SDK_INT >= 23 && ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED && ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            requestPermissions(
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                ), 100
            )
            return true
        }
        return false
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String?>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == 100) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED && grantResults[1] == PackageManager.PERMISSION_GRANTED) {
                enable_buttons()
            } else {
                runtime_permissions()
            }
        }
    }


    private fun enable_buttons() {

        val i = Intent(applicationContext, BackgrounLocationService::class.java)
        startService(i)
    }

    override fun onCreateDescription(): CharSequence? {
        return super.onCreateDescription()

        val i = Intent(applicationContext, BackgrounLocationService::class.java)
        stopService(i)
    }

}
