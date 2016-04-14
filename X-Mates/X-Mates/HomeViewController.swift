//
//  HomeViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 3/5/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit
import FBSDKCoreKit
import FBSDKLoginKit

class HomeViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
	
	@IBOutlet weak var dateLabel: UILabel!
	@IBOutlet weak var openMenuBar: UIBarButtonItem!
	
	private var appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
	
	let dummyActivities = ["Running", "Running", "Basketball"]
	let dummyDates = ["April 17, 2016", "April 22, 2016", " April 27, 2016"]
	
	private let userURL = "http://192.168.99.100:2000/user/"
	
	override func viewDidAppear(animated: Bool) {
		super.viewDidAppear(animated)
//		self.appDelegate.xmate.get(userURL, mode: "user")
	}
	
	override func viewDidLoad() {
		super.viewDidLoad()
		
		let formatter = NSDateFormatter()
		formatter.dateStyle = .LongStyle
		dateLabel.text = formatter.stringFromDate(NSDate())
		
		openMenuBar.target = self.revealViewController()
		openMenuBar.action = Selector("revealToggle:")
		
		self.view.addGestureRecognizer(self.revealViewController().panGestureRecognizer())
		
	}
	
	@IBAction func goToSearchExercise(sender: UIButton) {
		self.performSegueWithIdentifier("searchExercise", sender: self)
	}
	
	func numberOfSectionsInTableView(tableView: UITableView) -> Int {
		return 1
	}
	
	func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return self.dummyActivities.count
	}
	
	func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		
		let cell = tableView.dequeueReusableCellWithIdentifier("upcomingCell", forIndexPath: indexPath)
		cell.textLabel?.text = self.dummyActivities[indexPath.row]
		cell.detailTextLabel?.text = self.dummyDates[indexPath.row]
		
		return cell
	}

	
}
