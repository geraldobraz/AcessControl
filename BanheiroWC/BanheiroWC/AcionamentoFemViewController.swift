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

   let mqttClient = CocoaMQTT(clientID: "iOS Device", host:"192.168.1.2", port: 5050)
    
    
    @IBAction func SairLogin(_ sender: Any) {
        self.performSegue(withIdentifier: "sairLoginFem", sender: nil)
    }
    
    
    @IBAction func AcionarPorta(_ sender: Any) {
        mqttClient.subscribe("celular/porta")
        mqttClient.publish("celular/porta", withString: "FEM")
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
