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
    
    @IBOutlet weak var cpfUsuario: UITextField!
    @IBOutlet weak var senhaUsuario: UITextField!

    var cpf: String = "10760639426"
    var senha: String = "1234"
    var confirmCPF: Bool = false
    var confirmSENHA: Bool = false
    var x: Int = 0
    var aux: Bool = true
    var nome: String = ""
    var vaiCPF: String = ""
    let aciona = AcionamentoViewController()
    var wait: UIActivityIndicatorView = UIActivityIndicatorView()
    let mqttClient = CocoaMQTT(clientID: "iOS Device", host:"192.168.1.3", port: 5050) // Configurações do MQTT
    
    
    override func viewDidLoad() {
        mqttClient.connect()
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.setNavigationBarHidden(false, animated: false)
    }
    
///////
   
    
    // Func Alerta ************************************************************************************************
    func exibirMensagem(titulo: String, mensagem: String){
        let alerta = UIAlertController(title: titulo, message: mensagem, preferredStyle : .alert)
        let acaoOK = UIAlertAction(title:  "OK", style: .cancel, handler: nil)
        alerta.addAction(acaoOK)
        present(alerta, animated: true, completion: nil)
        
        // Ex.
        /*
         self.exibirMensagem(titulo: "Dados incorretos.", mensagem: "Senhas não são iguais")
         */
    }
//   ************************************************************************************************

//    @IBAction func Conectar(_ sender: UIButton) {
//        mqttClient.connect()
//    }
//    
    //TODO: Fazer o armazenamento dos dados ************************
    @IBAction func guardarDados(_ sender: UISwitch) {
        
        if(sender.isOn){
            print("Guardou")
        }else{
            print("Nao Guardou")
        }
        
    }
//************************************************************************************************
    
    @IBAction func loginButton(_ sender: UIButton) {
    
        // Rotina do icone de wait
         wait.center = self.view.center
         wait.hidesWhenStopped = true
         wait.activityIndicatorViewStyle = UIActivityIndicatorViewStyle.whiteLarge
         view.addSubview(wait)
         wait.startAnimating()
        
      
        // MQTT Configurações
        mqttClient.delegate = self
        // Subscribes do MQTT
        mqttClient.subscribe("celular/cpf")
        mqttClient.subscribe("celular/dados")
        mqttClient.subscribe("celular/dados/resposta")
        mqttClient.subscribe("celular/senha")
        mqttClient.subscribe("celular/cpf/confirmacao")
        mqttClient.subscribe("celular/senha/confirmacao")
        
        nome = cpfUsuario.text! + "$" + senhaUsuario.text!
        mqttClient.publish("celular/dados", withString: nome)
        

        
        
    }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        view.endEditing(true)
    }
    
    
}
// >> Salvar dados nos despositivos
/*
 UserDefaults.standard.set(<#T##value: Bool##Bool#>, forKey: <#T##String#>)
 UserDefaults.standard.object(forKey: <#T##String#>)
 UserDefaults.standard.removeObject(forKey: <#T##String#>)
 */



extension EntrarViewController: CocoaMQTTDelegate{
    
//    func mqtt(_ mqtt: CocoaMQTT, didReceive trust: SecTrust, completionHandler: @escaping (Bool) -> Void) {
//
//        completionHandler(true)
//    }
    
    func mqtt(_ mqtt: CocoaMQTT, didConnectAck ack: CocoaMQTTConnAck) {
        
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didPublishMessage message: CocoaMQTTMessage, id: UInt16) {
        
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didPublishAck id: UInt16) {
        
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didReceiveMessage message: CocoaMQTTMessage, id: UInt16) {
     
//        if(message.topic == "celular/cpf/confirmacao"){
//            if(message.string! == "ok"){
//                print("CPF OK!")
//                //self.performSegue(withIdentifier: "loginSegue", sender: nil)
//                confirmCPF = true
//            }
//
//        }
//        if(message.topic == "celular/senha/confirmacao"){
//            if(message.string! == "ok"){
//                print("SENHA OK!")
//                confirmSENHA = true
//            }
//
//        }
        
/*Teste
         
         
         
         */
      
        
        if(message.topic == "celular/dados/resposta"){
        
            
            if(message.string! == "Masc"){ // Masc
                wait.stopAnimating()
                self.performSegue(withIdentifier: "loginMasc", sender: nil) // FIXME: Colocar um segue para uma tela masc
            }
            
            if(message.string! == "Fem"){
                wait.stopAnimating()
                self.performSegue(withIdentifier: "loginFem", sender: nil)// FIXME: Colocar um segue para uma tela fem
            }
            
            
            if(message.string! == "nao"){
                wait.stopAnimating()
                exibirMensagem(titulo: "CPF ou senha incorretos", mensagem: "Digite novamente.")
            }
            
        }
        
        
        
// Antigo (Certo)
        
//        if(message.topic == "celular/dados/resposta"){
//           // let dados = message.string?.components(separatedBy: "%")
//
//            if(message.string! == "ok"){
//                wait.stopAnimating()
//                self.performSegue(withIdentifier: "loginSegue", sender: nil)
//            }
//            //if(message.string! == "nao ok"){
//            if(message.string! == "nao"){
//                wait.stopAnimating()
//                exibirMensagem(titulo: "CPF ou senha incorretos", mensagem: "Digite novamente.")
//            }
//
//        }
        
        
        
//         if((confirmCPF && confirmSENHA) && aux){
//         wait.stopAnimating()
//         self.performSegue(withIdentifier: "loginSegue", sender: nil)
//         }
//        if(aux == false){
//            exibirMensagem(titulo: "CPF ou senha incorretos", mensagem: "Digite novamente.")
//        }
        
        
        
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



