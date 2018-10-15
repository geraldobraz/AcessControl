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
    
    let mqttClient = CocoaMQTT(clientID: "iOS Device", host:"192.168.1.2", port: 5050)
    
    // Quit Login
    @IBAction func SairLogin(_ sender: Any) {
        self.performSegue(withIdentifier: "sairloginMasc", sender: nil)
        
    }
    
    // Open the door
    @IBAction func AcionarPorta(_ sender: Any) {
        mqttClient.subscribe("celular/porta/Masc")
        mqttClient.publish("celular/porta/Masc", withString: "ON")
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
