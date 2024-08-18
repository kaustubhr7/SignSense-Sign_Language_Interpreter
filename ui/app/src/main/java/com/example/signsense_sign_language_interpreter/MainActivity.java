package com.example.signsense_sign_language_interpreter;

import android.os.Bundle;
import android.view.SurfaceView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.lifecycle.LifecycleOwner;

public class MainActivity extends AppCompatActivity {

    private SurfaceView surfaceView;
    private CameraXHelper cameraXHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        surfaceView = findViewById(R.id.surfaceView);
        cameraXHelper = new CameraXHelper(this, surfaceView);

        // Start camera
        cameraXHelper.startCamera(this);
    }
}
