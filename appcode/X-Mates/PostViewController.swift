//
//  PostViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 4/13/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit
import FBSDKCoreKit
import FBSDKLoginKit
import CoreLocation

class PostViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, UIPickerViewDataSource, UIPickerViewDelegate {
	
	@IBOutlet weak var postTable: UITableView!
	@IBOutlet weak var matchTable: UITableView!
	@IBOutlet weak var matchLabel: UILabel!
	@IBOutlet weak var cancelButton: UIBarButtonItem!
	
	private let fields = ["Date", "Start Time", "End Time", "Categories"]
	private let catagoryList = ["Basketball", "Football", "Gym", "Swimming", "Running", "Vollyball"]
	private let scheduleURL = "http://192.168.99.100:4000/schedule/"
	private let messageURL = "http://192.168.99.100:4000/message/"
	
	private var appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
	private var catagory = "Basketball"
	private var startTime : NSTimeInterval = 0.0
	private var endTime : NSTimeInterval = 0.0
	private var receiverID = ""
	private var date = ""
	
	override func viewDidLoad() {
		super.viewDidLoad()
		// Do any additional setup after loading the view, typically from a nib.
		self.appDelegate.xmate.matches.removeAll()
	}
	
	func numberOfSectionsInTableView(tableView: UITableView) -> Int {
		return 1
	}
	
	func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		if tableView == postTable
		{
			return self.fields.count
		}
		else
		{
			return self.appDelegate.xmate.matches.count
		}
	}
	
	func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		if tableView == postTable
		{
			let cell = tableView.dequeueReusableCellWithIdentifier("fields", forIndexPath: indexPath)
			
			cell.textLabel?.text = fields[indexPath.row]
			
			return cell
		}
		else
		{
			let cell = tableView.dequeueReusableCellWithIdentifier("userinfo", forIndexPath: indexPath) as! MatchTableViewCell
			cell.userLabel.text = self.appDelegate.xmate.matches[indexPath.row]["username"] as? String
			
			cell.inviteButton.tag = indexPath.row
			cell.inviteButton.addTarget(self, action: #selector(PostViewController.inviteUser(_:)), forControlEvents: .TouchUpInside)
			
			return cell
		}
		
	}
	
	func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
		
		if tableView == self.postTable
		{
			let index = indexPath.row
			let cell = tableView.cellForRowAtIndexPath(indexPath)!
			
			switch index
			{
			case 0:
				datePicker(cell, mode: "Date")
				break
			case 1:
				datePicker(cell, mode: "Start Time")
				break
			case 2:
				datePicker(cell, mode: "End Time")
				break
			case 3:
				catagoryPicker(cell)
				break
			default:
				break
			}
		}
	}
	
	func numberOfComponentsInPickerView(pickerView: UIPickerView) -> Int {
		return 1
	}
	
	func pickerView(pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
		return self.catagoryList.count
	}
	
	func pickerView(pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
		return self.catagoryList[row]
	}
	
	func pickerView(pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
		print("Your favorite console is \(self.catagoryList[row])")
		self.catagory = self.catagoryList[row]
	}
	
	func datePicker(cell: UITableViewCell, mode: String) {
		
		let alertController = UIAlertController(title: "\n\n\n\n\n\n\n\n\n", message: nil, preferredStyle: UIAlertControllerStyle.ActionSheet)
		let datePicker = UIDatePicker(frame: CGRectMake(25, 0, 305, 200))
		let formatter = NSDateFormatter()
		
		datePicker.date = NSDate()
		if mode == "Date"
		{
			datePicker.datePickerMode = UIDatePickerMode.Date
			formatter.dateStyle = .MediumStyle
		}
		else if mode == "Start Time" || mode == "End Time"
		{
			datePicker.datePickerMode = UIDatePickerMode.Time
			formatter.dateFormat = "hh:mm a"
		}
		
		let done = UIAlertAction(title: "Done", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
			cell.detailTextLabel?.text = formatter.stringFromDate(datePicker.date)
			if mode == "Start Time"
			{
				self.startTime = datePicker.date.timeIntervalSince1970
			}
			else if mode == "End Time"
			{
				self.endTime = datePicker.date.timeIntervalSince1970
			}
			else if mode == "Date"
			{
				self.date = formatter.stringFromDate(datePicker.date)
			}
		})
		
		alertController.addAction(done)
		alertController.view.addSubview(datePicker)
		self.presentViewController(alertController, animated: true, completion: nil)
		
	}
	
	func catagoryPicker(cell: UITableViewCell) {
		
		let alertController = UIAlertController(title: "\n\n\n\n\n\n\n\n\n", message: nil, preferredStyle: UIAlertControllerStyle.ActionSheet)
		let catagoryPicker = UIPickerView(frame: CGRectMake(25, 0, 305, 200))
		catagoryPicker.dataSource = self
		catagoryPicker.delegate = self
		
		let done = UIAlertAction(title: "Done", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
			cell.detailTextLabel?.text = self.catagory
		})
		
		alertController.addAction(done)
		alertController.view.addSubview(catagoryPicker)
		self.presentViewController(alertController, animated: true, completion: nil)
		
	}
	
	@IBAction func cancelPost(sender: UIBarButtonItem) {
		self.performSegueWithIdentifier("cancelPost", sender: self)
	}
	
	@IBAction func postExercise(sender: UIBarButtonItem) {
		if self.endTime < self.startTime
		{
			let alertController = UIAlertController(title: "Invalid Post", message: "End Time must later than Start Time", preferredStyle: UIAlertControllerStyle.Alert)
			let done = UIAlertAction(title: "OK", style: UIAlertActionStyle.Default, handler: nil)
			alertController.addAction(done)
			self.presentViewController(alertController, animated: true, completion: nil)
		}
		else
		{
			self.appDelegate.xmate.schedule["creator"] = self.appDelegate.xmate.user["_id"]
			self.appDelegate.xmate.schedule["start_time"] = self.startTime
			self.appDelegate.xmate.schedule["end_time"] = self.endTime
			self.appDelegate.xmate.schedule["type"] = self.catagory
			self.appDelegate.xmate.schedule["date"] = self.date
			
			// create post
			self.appDelegate.xmate.post(self.scheduleURL, mode: "schedule")
			// find all matches for the post
			let data = ["pid":self.appDelegate.xmate.schedule["_id"]!, "uid":self.appDelegate.xmate.user["_id"]!, "start_time":self.startTime, "end_time":self.endTime, "type":self.catagory, "action":"match"]
			self.appDelegate.xmate.search(self.scheduleURL, data: data)
			
			self.postTable.userInteractionEnabled = false
			self.matchTable.reloadData()
			self.matchLabel.hidden = false
			self.matchTable.hidden = false
		}
	}
	
	@IBAction func inviteUser(sender: UIButton) {
		
		let alertController = UIAlertController(title: "Confirm Invitation", message: "", preferredStyle: UIAlertControllerStyle.Alert)
		
		let confirm = UIAlertAction(title: "Confirm", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
			let row = sender.tag
			self.receiverID = self.appDelegate.xmate.matches[row]["_id"] as! String
			self.appDelegate.xmate.post(self.messageURL, mode: "invite", id: self.receiverID)
		})
		let cancel = UIAlertAction(title: "Cancel", style: UIAlertActionStyle.Destructive, handler: nil)
		
		
		alertController.addAction(cancel)
		alertController.addAction(confirm)
		self.presentViewController(alertController, animated: true, completion: nil)
	}
	
}
