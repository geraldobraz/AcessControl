package com.example.geraldobraz.androidapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class LoginActivity extends AppCompatActivity {

    private EditText cpfField;
    private EditText passwordField;

    final static String serverUri = "tcp://192.168.1.2:5050";
    final static String clientId = "Android Device";
    final String subscriptionTopic = "celular/dados";
    final String responseTopic = "celular/dados/resposta";

    final static String GENDER_IDENTIFIER = "gender_identifier";
    final static String GENDER_MASC = "Masc";
    final static String GENDER_FEM = "Fem";
    final String USER_NOT_FOUND = "nao";

    private MqttAndroidClient mqttClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // barra do titulo
        if (getSupportActionBar() != null){
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setDisplayShowHomeEnabled(true);

            getSupportActionBar().setTitle(getString(R.string.login_screen_title));
        }

        // MQTT
        mqttClient = new MqttAndroidClient(getApplicationContext(), serverUri, clientId);
        try {
            mqttClient.connect();
        } catch (MqttException ex) {
            ex.printStackTrace();
        }
        mqttClient.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                if (topic.equals(responseTopic)) {
                    if (message.toString().equals(GENDER_MASC)) {
                        Intent intent = new Intent(LoginActivity.this, OpenActivity.class);
                        intent.putExtra(GENDER_IDENTIFIER, GENDER_MASC);
                        startActivity(intent);
                    } else if (message.toString().equals(GENDER_FEM)) {
                        Intent intent = new Intent(LoginActivity.this, OpenActivity.class);
                        intent.putExtra(GENDER_IDENTIFIER, GENDER_FEM);
                        startActivity(intent);
                    } else if (message.toString().equals(USER_NOT_FOUND)) {
                        passwordField.setError(getString(R.string.wrong_password));
                        passwordField.requestFocus();
                    }
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });

        cpfField = (EditText) findViewById(R.id.cpf_field);
        passwordField = (EditText) findViewById(R.id.password_field);

        Button loginBtn = (Button) findViewById(R.id.login_btn);
        loginBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String cpf = cpfField.getText().toString();
                String senha = passwordField.getText().toString();

                //chamar mqtt para verificar se o usuario está cadastrado
                try {
                    mqttClient.subscribe(subscriptionTopic, 0);
                    mqttClient.subscribe(responseTopic, 0);
                } catch (MqttException ex) {
                    ex.printStackTrace();
                }
                String nome = cpf + "$" + senha;
                MqttMessage mqttMessage = new MqttMessage(nome.getBytes());
                try {
                    mqttClient.publish(subscriptionTopic, mqttMessage);
                } catch (MqttException ex) {
                    ex.printStackTrace();
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

}

