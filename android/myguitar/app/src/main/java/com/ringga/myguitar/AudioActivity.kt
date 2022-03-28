package com.ringga.myguitar

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.ringga.myguitar.databinding.ActivityAudioBinding


class AudioActivity : AppCompatActivity() {

    private lateinit var binding: ActivityAudioBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityAudioBinding.inflate(layoutInflater)
        setContentView(binding.root)

       binding.button.setOnClickListener {
           getAudioMicrofon()
       }
    }

    private fun getAudioMicrofon() {


    }
}

