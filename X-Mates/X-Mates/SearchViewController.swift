//
//  SearchViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 3/6/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit
import FBSDKCoreKit
import FBSDKLoginKit

class SearchViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
	
	@IBOutlet weak var exerciseInfoTable: UITableView!
	@IBOutlet weak var searchResultTable: UITableView!
	
	let dummyTitles = ["Date", "Time", "Duration", "Categories"]
	let dummyInfos = ["Mar 11, 2016", "3 PM", "1 Hour", "Gym Workout"]
	let dummyResultTitles = ["Gym Workout", "Gym Workout", "Gym Workout", "Gym Workout", "Gym Workout"]
	let dummyResultDetails = ["Mar 11, 2016 - 2PM", "Mar 11, 2016 - 3PM", "Mar 11, 2016 - 3:30PM", "Mar 11, 2016 - 3PM", "Mar 12, 2016 - 3PM"]
	
	override func viewDidLoad() {
		super.viewDidLoad()
		// Do any additional setup after loading the view, typically from a nib.
	}
	
	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
		// Dispose of any resources that can be recreated.
	}
	
	@IBAction func cancelExerciseSearch(sender: UIBarButtonItem) {
		self.performSegueWithIdentifier("cancelSearch", sender: self)
	}
	
	func numberOfSectionsInTableView(tableView: UITableView) -> Int {
		return 1
	}
	
	func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		var count = 0;
		
		if tableView == exerciseInfoTable
		{
			count = self.dummyTitles.count
		}
//		else if tableView == searchResultTable
//		{
//			count = self.dummyResultTitles.count
//		}
		
		return count
	}
	
	func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		
		var cell = UITableViewCell()
		
		if tableView == exerciseInfoTable
		{
			cell = tableView.dequeueReusableCellWithIdentifier("postCell", forIndexPath: indexPath)
			cell.textLabel?.text = self.dummyTitles[indexPath.row]
			cell.detailTextLabel?.text = self.dummyInfos[indexPath.row]
			
		}
//		else if tableView == searchResultTable
//		{
//			cell = tableView.dequeueReusableCellWithIdentifier("resultCell", forIndexPath: indexPath)
//			cell.textLabel?.text = self.dummyResultTitles[indexPath.row]
//			cell.detailTextLabel?.text = self.dummyResultDetails[indexPath.row]
//		}
		
		return cell
	}
	
}
