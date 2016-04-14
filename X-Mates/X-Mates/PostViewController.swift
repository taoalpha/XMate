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

class PostViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, UIPickerViewDataSource, UIPickerViewDelegate {
	
	private let fields = ["Date", "Start Time", "End Time", "Categories"]
	private let catagoryList = ["Basketball", "Football", "Gym Workout", "Swimming", "Running", "Vollyball"]
	private let scheduleURL = "http://192.168.99.100:2000/schedule/"
	
	private var appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
	private var catagory = ""
	private var startTime : NSTimeInterval = 0.0
	private var endTime : NSTimeInterval = 0.0
	
	
	override func viewDidLoad() {
		super.viewDidLoad()
		// Do any additional setup after loading the view, typically from a nib.
		
	}
	
	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
		// Dispose of any resources that can be recreated.
	}
	
	@IBAction func cancelExerciseSearch(sender: UIBarButtonItem) {
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
			//self.appDelegate.xmate.post(scheduleURL, mode: "schedule")
		}
	}
	
	func numberOfSectionsInTableView(tableView: UITableView) -> Int {
		return 1
	}
	
	func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		
		return self.fields.count
	}
	
	func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		
		let cell = tableView.dequeueReusableCellWithIdentifier("test", forIndexPath: indexPath)
		cell.textLabel?.text = fields[indexPath.row]
		
		return cell
	}
	
	func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
		
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
	
	func durationPicker(cell: UITableViewCell) {
		
		let alertController = UIAlertController(title: "\n\n\n\n\n\n\n\n\n", message: nil, preferredStyle: UIAlertControllerStyle.ActionSheet)
		let durationPicker = UIPickerView(frame: CGRectMake(25, 0, 305, 200))
		durationPicker.dataSource = self
		durationPicker.delegate = self
		
		let done = UIAlertAction(title: "Done", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
			cell.detailTextLabel?.text = self.catagory
		})
		
		alertController.addAction(done)
		alertController.view.addSubview(durationPicker)
		self.presentViewController(alertController, animated: true, completion: nil)

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
	
}
