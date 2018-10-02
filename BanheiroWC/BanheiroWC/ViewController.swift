//
//  ViewController.swift
//  BanheiroWC
//
//  Created by Geraldo Neto on 31/01/18.
//  Copyright © 2018 Geraldo Neto. All rights reserved.
//

import UIKit




class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }

    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.setNavigationBarHidden(true, animated: false)
    }
    
}

