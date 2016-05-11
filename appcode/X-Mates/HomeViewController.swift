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
	@IBOutlet weak var activityTable: UITableView!
	
	private let userURL = "http://192.168.99.100:4000/user/"
	private let scheduleURL = "http://192.168.99.100:4000/schedule/"
	
	private var appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
	private var typeList = [String]()
	private var dateList = [String]()
	
	override func viewDidAppear(animated: Bool) {
		super.viewDidAppear(animated)
		//self.appDelegate.xmate.get(userURL, mode: "user")
		//print(self.appDelegate.xmate.user)
		self.getSchedules()
		self.activityTable.reloadData()
	}
	
	override func viewDidLoad() {
		super.viewDidLoad()
		
		let formatter = NSDateFormatter()
		formatter.dateStyle = .LongStyle
		dateLabel.text = formatter.stringFromDate(NSDate())
		
		openMenuBar.target = self.revealViewController()
		openMenuBar.action = #selector(SWRevealViewController.revealToggle(_:))
		
		self.view.addGestureRecognizer(self.revealViewController().panGestureRecognizer())
		self.appDelegate.xmate.get(userURL, mode: "user")
		print(self.appDelegate.xmate.user)
		
	}
	
	@IBAction func goToSearchExercise(sender: UIButton) {
		self.performSegueWithIdentifier("searchExercise", sender: self)
	}
	
	func numberOfSectionsInTableView(tableView: UITableView) -> Int {
		if self.typeList.count == 0
		{
			let defaultMsg = UILabel()
			defaultMsg.textAlignment = NSTextAlignment.Center
			defaultMsg.textColor = UIColor.lightGrayColor()
			defaultMsg.text = "No Activity"
			tableView.separatorStyle = UITableViewCellSeparatorStyle.None
			tableView.backgroundView = defaultMsg
			return 0
		}
		else{
			tableView.backgroundView = nil
			return 1
		}
	}
	
	func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return self.typeList.count
	}
	
	func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		
		let cell = tableView.dequeueReusableCellWithIdentifier("upcomingCell", forIndexPath: indexPath) as! ActivityTableViewCell
		if self.typeList.count != 0
		{
			cell.dateLabel.text = self.dateList[indexPath.row]
			cell.typeLabel.text = self.typeList[indexPath.row]
		}
		
		return cell
	}

	private func getSchedules() {
		self.typeList.removeAll()
		self.dateList.removeAll()
		let list = self.appDelegate.xmate.user["schedule_list"] as! [String]
		if list.count != 0
		{
			for index in 0...list.count-1
			{
				let sid = list[index]
				self.appDelegate.xmate.get(self.scheduleURL, mode: "schedule", id: sid)
				self.typeList.append(self.appDelegate.xmate.schedule["type"] as! String)
				self.dateList.append(self.appDelegate.xmate.schedule["date"] as! String)
			}
		}
	}
	
}
