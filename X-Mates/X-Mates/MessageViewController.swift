//
//  MessageViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 4/14/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit

class MessageViewController: UITableViewController {

	@IBOutlet weak var openMenuBar: UIBarButtonItem!
	
	override func viewDidLoad() {
		openMenuBar.target = self.revealViewController()
		openMenuBar.action = Selector("revealToggle:")
		
		self.view.addGestureRecognizer(self.revealViewController().panGestureRecognizer())
	}
	
}
