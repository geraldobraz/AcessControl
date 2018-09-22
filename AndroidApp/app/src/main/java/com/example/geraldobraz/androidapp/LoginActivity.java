package com.example.geraldobraz.androidapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import helpers.MQTTHelper;

public class LoginActivity extends AppCompatActivity {

    private EditText cpfField;
    private EditText passwordField;

    private MQTTHelper mqttHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        if (getSupportActionBar() != null){
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setDisplayShowHomeEnabled(true);

            getSupportActionBar().setTitle(getString(R.string.login_screen_title));
        }

        cpfField = (EditText) findViewById(R.id.cpf_field);
        passwordField = (EditText) findViewById(R.id.password_field);

        Button loginBtn = (Button) findViewById(R.id.login_btn);
        loginBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String cpf = cpfField.getText().toString();
                String senha = passwordField.getText().toString();

                Log.d("LOGIN", "cpf: " + cpf);
                Log.d("LOGIN", "senha: " + senha);

                //chamar mqtt para verificar se o usuario está cadastrado
                startMqtt();

                if (cpf.equals("10121975495") && senha.equals("1234")) {
                    Intent intent = new Intent(LoginActivity.this, OpenActivity.class);
                    startActivity(intent);
                } else {
                    passwordField.setError(getString(R.string.wrong_password));
                    passwordField.requestFocus();
                }
            }
        });
    }

    // voltar para tela anteior quando a seta é clicada
    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }

    private void startMqtt(){
        mqttHelper = new MQTTHelper(getApplicationContext());
        mqttHelper.mqttAndroidClient.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean b, String s) {
                Log.w("Debug","Connected");
            }

            @Override
            public void connectionLost(Throwable throwable) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage mqttMessage) throws Exception {
                Log.w("Debug",mqttMessage.toString());
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {

            }
        });
    }
}

