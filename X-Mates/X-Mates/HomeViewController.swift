//
//  HomeViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 3/5/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit

class HomeViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
	
	@IBOutlet weak var dateLabel: UILabel!
	@IBOutlet weak var openMenuBar: UIBarButtonItem!
	
	let dummyActivities = ["Running", "Basketball", "Gym Workout"]
	let dummyDates = ["Mar 21, 2016", "Mar 28, 2016", " Mar 29, 2016"]
	
	override func viewDidLoad() {
		super.viewDidLoad()
		
		let formatter = NSDateFormatter()
		formatter.dateStyle = .LongStyle
		dateLabel.text = formatter.stringFromDate(NSDate())
		
		openMenuBar.target = self.revealViewController()
		openMenuBar.action = Selector("revealToggle:")
		
		self.view.addGestureRecognizer(self.revealViewController().panGestureRecognizer())
	}
	
	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
		// Dispose of any resources that can be recreated.
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
