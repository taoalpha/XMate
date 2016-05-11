//
//  HistoryViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 4/14/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit

class HistoryViewController: UITableViewController {
	
	@IBOutlet weak var openMenuBar: UIBarButtonItem!
	
	let dummyActivities = ["Running", "Basketball", "Gym Workout", "Running"]
	let dummyDates = ["Mar 21, 2016", "Mar 28, 2016", "Mar 29, 2016", " April 3, 2016"]
	
	override func viewDidLoad() {
		openMenuBar.target = self.revealViewController()
		openMenuBar.action = #selector(SWRevealViewController.revealToggle(_:))
		
		self.view.addGestureRecognizer(self.revealViewController().panGestureRecognizer())
	}
	
	override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
		return 1
	}
	
	override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return self.dummyActivities.count
	}
	
	override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCellWithIdentifier("history", forIndexPath: indexPath)
		let index = indexPath.row
		
		cell.textLabel?.text = self.dummyActivities[index]
		cell.detailTextLabel?.text = self.dummyDates[index]
		
		return cell
	}
}
