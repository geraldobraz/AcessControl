//
//  AcionamentoViewController.swift
//  BanheiroWC
//
//  Created by Geraldo Neto on 31/01/18.
//  Copyright © 2018 Geraldo Neto. All rights reserved.
//


import UIKit
import CocoaMQTT

class AcionamentoViewController: UIViewController {
    var resposta: String = ""
    var aux: String!
    let mqttClient = CocoaMQTT(clientID: "iOS Device", host:"192.168.1.3", port: 5050)
    
    
    // Sair do Login
    @IBAction func SairLogin(_ sender: Any) {
        //exibirMensagem(titulo: "Deseja sair?", mensagem: "")
        self.performSegue(withIdentifier: "sairLogin", sender: nil)
        
    }
    // Acionar a Porta
    @IBAction func AcionarPorta(_ sender: Any) {
    
//        resposta = "_ON"
        mqttClient.subscribe("celular/porta")
        mqttClient.publish("celular/porta", withString: "ON")
    }
    
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
        self.navigationController?.setNavigationBarHidden(true, animated: false)
    }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
