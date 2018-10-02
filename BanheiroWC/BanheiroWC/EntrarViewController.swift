//
//  EntrarViewController.swift
//  BanheiroWC
//
//  Created by Geraldo Neto on 31/01/18.
//  Copyright © 2018 Geraldo Neto. All rights reserved.
//

import UIKit
import CocoaMQTT

class EntrarViewController: UIViewController {
    
    @IBOutlet weak var userCPF: UITextField!
    @IBOutlet weak var userPassword: UITextField!

    // Global Variables
    var userData: String = ""
    var wait: UIActivityIndicatorView = UIActivityIndicatorView()
    let mqttClient = CocoaMQTT(clientID: "iOS Device", host:"192.168.1.3", port: 5050) // Configurações do MQTT
    
    
    override func viewDidLoad() {
        mqttClient.connect() // Connecting on the broker
        super.viewDidLoad()
    }
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.setNavigationBarHidden(false, animated: false)
    }
    
    // Warning Function
    func exibirMensagem(titulo: String, mensagem: String){
        let alerta = UIAlertController(title: titulo, message: mensagem, preferredStyle : .alert)
        let acaoOK = UIAlertAction(title:  "OK", style: .cancel, handler: nil)
        alerta.addAction(acaoOK)
        present(alerta, animated: true, completion: nil)
    }

    @IBAction func loginButton(_ sender: UIButton) {
    
        // Wait rotine
         wait.center = self.view.center
         wait.hidesWhenStopped = true
         wait.activityIndicatorViewStyle = UIActivityIndicatorViewStyle.whiteLarge
         view.addSubview(wait)
         wait.startAnimating()
        
      
    // MQTT Configuration
        mqttClient.delegate = self
        // MQTT's Topics
        mqttClient.subscribe("celular/cpf")
        mqttClient.subscribe("celular/senha")
        mqttClient.subscribe("celular/dados")
        mqttClient.subscribe("celular/dados/resposta")
    
        userData = userCPF.text! + "$" + userPassword.text!
        mqttClient.publish("celular/dados", withString: userData)
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        view.endEditing(true)
    }
    
    
}


extension EntrarViewController: CocoaMQTTDelegate{
    
    func mqtt(_ mqtt: CocoaMQTT, didConnectAck ack: CocoaMQTTConnAck) {
        
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didPublishMessage message: CocoaMQTTMessage, id: UInt16) {
        
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didPublishAck id: UInt16) {
        
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didReceiveMessage message: CocoaMQTTMessage, id: UInt16) {
        
        if(message.topic == "celular/dados/resposta"){
        
            // Masculine
            if(message.string! == "Masc"){
                wait.stopAnimating()
                self.performSegue(withIdentifier: "loginMasc", sender: nil)
            }
            // Feminine
            if(message.string! == "Fem"){
                wait.stopAnimating()
                self.performSegue(withIdentifier: "loginFem", sender: nil)
            }
            
            
            if(message.string! == "nao"){
                wait.stopAnimating()
                exibirMensagem(titulo: "CPF ou senha incorretos", mensagem: "Digite novamente.")
            }
            
        }
        
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didSubscribeTopic topic: String) {
        
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didUnsubscribeTopic topic: String) {
        
    }
    
    func mqttDidPing(_ mqtt: CocoaMQTT) {
        
    }
    
    func mqttDidReceivePong(_ mqtt: CocoaMQTT) {
        
    }
    
    func mqttDidDisconnect(_ mqtt: CocoaMQTT, withError err: Error?) {
        
    }
    
    
    
    
}



