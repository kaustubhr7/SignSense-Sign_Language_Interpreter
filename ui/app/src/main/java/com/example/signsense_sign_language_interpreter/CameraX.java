package com.example.signsense_sign_language_interpreter;

import android.content.Context;
import android.util.Log;
import android.util.Size;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

import androidx.camera.core.CameraSelector;
import androidx.camera.core.ImageAnalysis;
import androidx.camera.core.ImageProxy;
import androidx.camera.core.Preview;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.lifecycle.LifecycleOwner;

import java.util.concurrent.ExecutionException;

public class CameraXHelper {

    private static final String TAG = "CameraXHelper";
    private final Context context;
    private final SurfaceView surfaceView;

    public CameraXHelper(Context context, SurfaceView surfaceView) {
        this.context = context;
        this.surfaceView = surfaceView;
    }

    public void startCamera(LifecycleOwner lifecycleOwner) {
        ProcessCameraProvider cameraProviderFuture = ProcessCameraProvider.getInstance(context);

        cameraProviderFuture.addListener(() -> {
            try {
                ProcessCameraProvider cameraProvider = cameraProviderFuture.get();

                Preview preview = new Preview.Builder()
                        .setTargetResolution(new Size(1280, 720))
                        .build();

                preview.setSurfaceProvider(surfaceView.getSurfaceProvider());

                ImageAnalysis imageAnalysis = new ImageAnalysis.Builder()
                        .setTargetResolution(new Size(1280, 720))
                        .build();

                imageAnalysis.setAnalyzer(ContextCompat.getMainExecutor(context), new HandAnalyzer());

                CameraSelector cameraSelector = new CameraSelector.Builder()
                        .requireLensFacing(CameraSelector.LENS_FACING_BACK)
                        .build();

                cameraProvider.bindToLifecycle(lifecycleOwner, cameraSelector, preview, imageAnalysis);

            } catch (ExecutionException | InterruptedException e) {
                Log.e(TAG, "Failed to bind camera use cases", e);
            }
        }, ContextCompat.getMainExecutor(context));
    }
}
