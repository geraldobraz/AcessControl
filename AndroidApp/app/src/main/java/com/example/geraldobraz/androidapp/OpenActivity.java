package com.example.geraldobraz.androidapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

public class OpenActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_open);

        if (getSupportActionBar() != null){
            getSupportActionBar().setTitle(getString(R.string.open_screen_title));
        }

        Button openBtn = (Button) findViewById(R.id.open_btn);
        openBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });

        Button entrarBtn = (Button) findViewById(R.id.sair_btn);
        entrarBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(OpenActivity.this, MainActivity.class);
                startActivity(intent);
            }
        });

        Button ajudaBtn = (Button) findViewById(R.id.ajuda2_btn);
        ajudaBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(OpenActivity.this, HelpActivity.class);
                startActivity(intent);
            }
        });

    }
}
