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

class SearchViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, UIPickerViewDataSource, UIPickerViewDelegate {
	
	@IBOutlet weak var exerciseInfoTable: UITableView!
	@IBOutlet weak var searchResultTable: UITableView!
	@IBOutlet weak var activityLabel: UILabel!
	
	private let fields = ["Date", "Start Time", "End Time", "Categories"]
	private let catagoryList = ["Basketball", "Football", "Gym", "Swimming", "Running", "Vollyball"]
	private let scheduleURL = "http://192.168.99.100:4000/schedule/"
	private let messageURL = "http://192.168.99.100:4000/message/"
	
	private var appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
	private var catagory = ""
	private var startTime : NSTimeInterval = 0.0
	private var endTime : NSTimeInterval = 0.0
	private var date = ""
	private var receiverID = ""
	
	override func viewDidLoad() {
		super.viewDidLoad()
		// Do any additional setup after loading the view, typically from a nib.
		self.appDelegate.xmate.matches.removeAll()
	}
	
	func numberOfSectionsInTableView(tableView: UITableView) -> Int {
		if tableView == self.searchResultTable
		{
			if self.appDelegate.xmate.matches.count == 0
			{
				let defaultMsg = UILabel()
				defaultMsg.textAlignment = NSTextAlignment.Center
				defaultMsg.textColor = UIColor.lightGrayColor()
				defaultMsg.text = "No Match"
				tableView.separatorStyle = UITableViewCellSeparatorStyle.None
				tableView.backgroundView = defaultMsg
				return 0
			}
			else{
				tableView.backgroundView = nil
				return 1
			}
		}
		else
		{
			return 1
		}
	}
	
	func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		if tableView == self.exerciseInfoTable
		{
			return self.fields.count
		}
		else
		{
			return self.appDelegate.xmate.matches.count
		}
	}
	
	func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		if tableView == self.exerciseInfoTable
		{
			let cell = tableView.dequeueReusableCellWithIdentifier("searchCell", forIndexPath: indexPath)
			
			cell.textLabel?.text = fields[indexPath.row]
			
			return cell
		}
		else
		{
			let cell = tableView.dequeueReusableCellWithIdentifier("resultCell", forIndexPath: indexPath) as! SearchTableViewCell
			
			let formatter = NSDateFormatter()
			formatter.dateFormat = "MMM-dd-YYYY hh:mm a"
			
			cell.userLabel.text = self.appDelegate.xmate.matches[indexPath.row]["username"] as? String
			if self.appDelegate.xmate.matches[indexPath.row]["start_time"] != nil
			{
				cell.userLabel.text = self.appDelegate.xmate.matches[indexPath.row]["creator"] as? String
				let st = self.appDelegate.xmate.matches[indexPath.row]["start_time"] as! NSTimeInterval
				let nsdate = NSDate(timeIntervalSince1970: st)
				cell.startLabel.text = formatter.stringFromDate(nsdate)

			}			
			cell.joinButton.tag = indexPath.row
			cell.joinButton.addTarget(self, action: #selector(SearchViewController.joinUser(_:)), forControlEvents: .TouchUpInside)
			
			return cell
		}
		
	}
	
	func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
		
		if tableView == self.exerciseInfoTable
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
		else
		{
			
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
	
	@IBAction func cancelSearch(sender: UIBarButtonItem) {
		self.performSegueWithIdentifier("cancelSearch", sender: self)
	}
	
	@IBAction func searchExercise(sender: UIBarButtonItem) {
		if self.endTime < self.startTime
		{
			let alertController = UIAlertController(title: "Invalid Search", message: "End Time must later than Start Time", preferredStyle: UIAlertControllerStyle.Alert)
			let done = UIAlertAction(title: "OK", style: UIAlertActionStyle.Default, handler: nil)
			alertController.addAction(done)
			self.presentViewController(alertController, animated: true, completion: nil)
		}
		else
		{
			// find all matches for the search
			var data = NSMutableDictionary(dictionary: ["action":"search"])
			if self.startTime != 0.0
			{
				data["start_time"] = self.startTime
			}
			if self.endTime != 0.0
			{
				data["end_time"] = self.endTime
			}
			if self.catagory != ""
			{
				data["type"] = self.catagory
			}
			
			print(data)
			
			let res = self.appDelegate.xmate.search(self.scheduleURL, data: NSDictionary(dictionary: data) as! [String : AnyObject])
			
			if res == "Server Error"
			{
				let alertController = UIAlertController(title: "ERROR", message: "Connection Error\nPlease Try Later", preferredStyle: UIAlertControllerStyle.Alert)
				
				let ok = UIAlertAction(title: "Ok", style: UIAlertActionStyle.Default, handler: nil)
				
				alertController.addAction(ok)
				self.presentViewController(alertController, animated: true, completion: nil)
			}
			
			self.searchResultTable.reloadData()
			self.searchResultTable.hidden = false
		}
	}
	
	@IBAction func joinUser(sender: UIButton) {
		let alertController = UIAlertController(title: "Confirm Join", message: "", preferredStyle: UIAlertControllerStyle.Alert)
		
		let join = UIAlertAction(title: "Join", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
			let row = sender.tag
			self.receiverID = self.appDelegate.xmate.matches[row]["_id"] as! String
			self.appDelegate.xmate.post(self.messageURL, mode: "join", id: self.receiverID)
		})
		let cancel = UIAlertAction(title: "Cancel", style: UIAlertActionStyle.Destructive, handler: nil)
		
		alertController.addAction(cancel)
		alertController.addAction(join)
		self.presentViewController(alertController, animated: true, completion: nil)
	}
}
