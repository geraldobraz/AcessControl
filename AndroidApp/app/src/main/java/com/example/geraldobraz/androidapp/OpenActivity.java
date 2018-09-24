package com.example.geraldobraz.androidapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class OpenActivity extends AppCompatActivity {

    final String mascDoorTopic = "celular/porta/Masc";
    final String femDoorTopic = "celular/porta/Fem";

    final String ON = "ON";
    private MqttAndroidClient mqttClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_open);

        if (getSupportActionBar() != null){
            getSupportActionBar().setTitle(getString(R.string.open_screen_title));
        }

        // Get data from intent
        Intent intent = getIntent();
        final String gender = intent.getStringExtra(LoginActivity.GENDER_IDENTIFIER);

        // MQTT config
        mqttClient = new MqttAndroidClient(getApplicationContext(), LoginActivity.serverUri, LoginActivity.clientId);
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

            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });

        Button openBtn = (Button) findViewById(R.id.open_door_btn);
        openBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    mqttClient.subscribe(femDoorTopic, 0);
                    mqttClient.subscribe(mascDoorTopic, 0);
                } catch (MqttException ex) {
                    ex.printStackTrace();
                }
                MqttMessage mqttMessage = new MqttMessage(ON.getBytes());
                try {
                    if (gender.equals(LoginActivity.GENDER_MASC)) {
                        mqttClient.publish(mascDoorTopic, mqttMessage);
                    } else if (gender.equals(LoginActivity.GENDER_FEM)) {
                        mqttClient.publish(femDoorTopic, mqttMessage);
                    }

                } catch (MqttException ex) {
                    ex.printStackTrace();
                }
            }
        });

        Button leaveBtn = (Button) findViewById(R.id.leave_btn);
        leaveBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(OpenActivity.this, MainActivity.class);
                startActivity(intent);
            }
        });
    }
}
