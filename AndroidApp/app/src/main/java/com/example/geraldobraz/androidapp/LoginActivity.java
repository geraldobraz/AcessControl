package com.example.geraldobraz.androidapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
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
    final String dataTopic = "celular/dados";
    final String responseDataTopic = "celular/dados/resposta";


    final static String GENDER_IDENTIFIER = "gender_identifier";
    final static String GENDER_MASC = "Masc";
    final static String GENDER_FEM = "Fem";
    final String USER_NOT_FOUND = "nao";


    private MqttAndroidClient mqttClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // Title
        if (getSupportActionBar() != null){
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setDisplayShowHomeEnabled(true);

            getSupportActionBar().setTitle(getString(R.string.login_screen_title));
        }

        // MQTT config
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
                if (topic.equals(responseDataTopic)) {
                    if (message.toString().equals(GENDER_MASC)) {
                        Intent intent = new Intent(LoginActivity.this, OpenActivity.class);
                        intent.putExtra(GENDER_IDENTIFIER, GENDER_MASC);
                        startActivity(intent);
                    } else if (message.toString().equals(GENDER_FEM)) {
                        Intent intent = new Intent(LoginActivity.this, OpenActivity.class);
                        intent.putExtra(GENDER_IDENTIFIER, GENDER_FEM);
                        startActivity(intent);
                    } else if (message.toString().equals(USER_NOT_FOUND)) {
                        passwordField.setError(getString(R.string.login_error));
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
                String password = passwordField.getText().toString();

                //Sending the data from user to the server
                try {
                    mqttClient.subscribe(dataTopic, 0);
                    mqttClient.subscribe(responseDataTopic, 0);
                } catch (MqttException ex) {
                    ex.printStackTrace();
                }
                String data = cpf + "$" + password;
                MqttMessage mqttMessage = new MqttMessage(data.getBytes());
                try {
                    mqttClient.publish(dataTopic, mqttMessage);
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

