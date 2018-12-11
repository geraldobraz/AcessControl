//
//  AcionamentoFemViewController.swift
//  BanheiroWC
//
//  Created by Geraldo Neto on 11/05/18.
//  Copyright © 2018 Geraldo Neto. All rights reserved.
//

import UIKit
import CocoaMQTT

class AcionamentoFemViewController: UIViewController {

   let mqttClient = CocoaMQTT(clientID: "iOS Device", host:"192.168.1.3", port: 5050)
    
    // Quit Login
    @IBAction func SairLogin(_ sender: Any) {
        self.performSegue(withIdentifier: "sairLoginFem", sender: nil)
    }
    
    // Open the Door
    @IBAction func AcionarPorta(_ sender: Any) {
        mqttClient.subscribe("celular/porta/Fem")
        mqttClient.publish("celular/porta/Fem", withString: "ON")
    }
    
    //Connect on the Broker
    override func viewDidLoad() {
        mqttClient.connect()
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.setNavigationBarHidden(true, animated: false)
    }

}
