//
//  MenuBarViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 3/7/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit

class MenuBarViewController: UITableViewController {
	
	var menuList = [String]()
	
	override func viewDidLoad() {
		self.menuList = ["Home", "Porfile", "Log Workout", "Settings"]
	}
	
	override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return self.menuList.count
	}
	
	override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCellWithIdentifier("menuCell", forIndexPath: indexPath)
		
		cell.textLabel?.text = menuList[indexPath.row]
		
		return cell
	}

}
