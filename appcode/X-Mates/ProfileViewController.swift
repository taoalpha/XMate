//
//  ProfileViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 3/5/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit
import FBSDKCoreKit
import FBSDKLoginKit
import CoreLocation

class ProfileViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, UIPickerViewDataSource, UIPickerViewDelegate {
	
	@IBOutlet weak var firstName: UITextField!
	@IBOutlet weak var lastName: UITextField!
	@IBOutlet weak var email: UITextField!
	
	private let SUCCESSE_STATUS = "1"
	private let userURL = "http://192.168.99.100:4000/user/"
	private let tableData = ["Gender", "Birthdate", "Height", "Weight"]
	private let feetList = ["0'", "1'", "2'", "3'", "4'", "5'", "6'", "7'"]
	private let inchList = ["0\"", "1\"", "2\"", "3\"", "4\"", "5\"", "6\"", "7\"", "8\"", "9\"", "10\"", "11\"", "12\""]
	private let weightList = ["90 - 110 lbs", "110 - 130 lbs", "130 - 150 lbs", "150 - 170 lbs", "170 - 190 lbs", "190 - 210 lbs"]
	private let normWeight = ["100", "120", "140", "160", "180", "200"]
	private let heightPicker = UIPickerView(frame: CGRectMake(25, 0, 305, 200))
	private let weightPicker = UIPickerView(frame: CGRectMake(25, 0, 305, 200))
	
	private var appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
	private var gender = "Male"
	private var birthday = ""
	private var height = "0' 0\""
	private var weight = "90 - 110 lbs"
		
	override func viewDidLoad() {
		super.viewDidLoad()
		
//		self.firstName.text = self.appDelegate.xmate.user["first_name"] as? String
//		self.lastName.text = self.appDelegate.xmate.user["last_name"] as? String
//		self.email.text = self.appDelegate.xmate.user["email"] as? String

	}
	
	override func viewDidAppear(animated: Bool) {
		print(self.appDelegate.xmate.user)
		self.firstName.text = self.appDelegate.xmate.user["first_name"] as? String
		self.lastName.text = self.appDelegate.xmate.user["last_name"] as? String
		self.email.text = self.appDelegate.xmate.user["email"] as? String
	}
	
	func numberOfSectionsInTableView(tableView: UITableView) -> Int {
		return 1
	}
	
	func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return self.tableData.count
	}
	
	func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCellWithIdentifier(self.tableData[indexPath.row], forIndexPath: indexPath)
		let index = indexPath.row
		
		cell.textLabel?.text = self.tableData[index]
		
		if index == 0
		{
			cell.detailTextLabel?.text = self.appDelegate.xmate.user["gender"] as? String
		}
		
		return cell
	}

	func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
		
		let index = indexPath.row
		let cell = tableView.cellForRowAtIndexPath(indexPath)!
		
		switch index
		{
		case 0:
			genderPicker(cell)
			break
		case 1:
			birthdatePicker(cell)
			break
		case 2:
			heightPicker(cell)
			break
		case 3:
			weightPicker(cell)
			break
		default:
			break
		}
	}
	
	func numberOfComponentsInPickerView(pickerView: UIPickerView) -> Int {
		if pickerView == heightPicker
		{
			return 2
		}
		else
		{
			return 1
		}
	}
	
	func pickerView(pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
		if pickerView == heightPicker
		{
			if component == 0
			{
				return self.feetList.count
			}
			else
			{
				return self.inchList.count
			}
		}
		else
		{
			return self.weightList.count
		}
	}
	
	func pickerView(pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
		if pickerView == heightPicker
		{
			if component == 0
			{
				return self.feetList[row]
			}
			else
			{
				return self.inchList[row]
			}
		}
		else
		{
			return self.weightList[row]
		}
	}
	
	func pickerView(pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
		if pickerView == heightPicker
		{
			self.height = feetList[pickerView.selectedRowInComponent(0)] + " " + inchList[pickerView.selectedRowInComponent(1)]
		}
		else
		{
			self.weight = weightList[row]
		}
	}
	
	func genderPicker(cell: UITableViewCell) {
		let alertController = UIAlertController(title:nil, message: nil, preferredStyle: UIAlertControllerStyle.ActionSheet)
		let male = UIAlertAction(title: "Male", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
			cell.detailTextLabel?.text = "Male"
			self.gender = (cell.detailTextLabel?.text)!
		})
		let female = UIAlertAction(title: "Female", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
			cell.detailTextLabel?.text = "Female"
			self.gender = (cell.detailTextLabel?.text)!
		})
		
		alertController.addAction(male)
		alertController.addAction(female)
		
		self.presentViewController(alertController, animated: true, completion: nil)
	}
	
	func birthdatePicker(cell: UITableViewCell) {
		
		let alertController = UIAlertController(title: "\n\n\n\n\n\n\n\n\n", message: nil, preferredStyle: UIAlertControllerStyle.ActionSheet)
		let datePicker = UIDatePicker(frame: CGRectMake(25, 0, 305, 200))
		let formatter = NSDateFormatter()
		
		datePicker.datePickerMode = UIDatePickerMode.Date
		datePicker.date = NSDate()
		formatter.dateStyle = .MediumStyle
		
		let done = UIAlertAction(title: "Done", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
			cell.detailTextLabel?.text = formatter.stringFromDate(datePicker.date)
			self.birthday = (cell.detailTextLabel?.text)!
		})
		
		alertController.addAction(done)
		alertController.view.addSubview(datePicker)
		self.presentViewController(alertController, animated: true, completion: nil)
	}
	
	func weightPicker(cell: UITableViewCell) {
		
		let alertController = UIAlertController(title: "\n\n\n\n\n\n\n\n\n", message: nil, preferredStyle: UIAlertControllerStyle.ActionSheet)
		
		weightPicker.dataSource = self
		weightPicker.delegate = self
		
		let done = UIAlertAction(title: "Done", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
			cell.detailTextLabel?.text = self.weight
		})
		
		alertController.addAction(done)
		alertController.view.addSubview(weightPicker)
		self.presentViewController(alertController, animated: true, completion: nil)
	}
	
	func heightPicker(cell: UITableViewCell) {
		
		let alertController = UIAlertController(title: "\n\n\n\n\n\n\n\n\n", message: nil, preferredStyle: UIAlertControllerStyle.ActionSheet)
		
		heightPicker.dataSource = self
		heightPicker.delegate = self
		
		let done = UIAlertAction(title: "Done", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
			cell.detailTextLabel?.text = self.height
		})
		
		alertController.addAction(done)
		alertController.view.addSubview(heightPicker)
		self.presentViewController(alertController, animated: true, completion: nil)
		
	}
	
	@IBAction func goToHome(sender: UIBarButtonItem) {
		
		self.appDelegate.xmate.user["first_name"] = firstName.text
		self.appDelegate.xmate.user["last_name"] = lastName.text
		self.appDelegate.xmate.user["email"] = email.text
		
		self.appDelegate.xmate.user["gender"] = self.gender
		self.appDelegate.xmate.user["birthday"] = self.birthday
		self.appDelegate.xmate.user["height"] = self.height
		self.appDelegate.xmate.user["weight"] = self.weight
		
		self.appDelegate.xmate.post(self.userURL, mode: "user")
		
		self.performSegueWithIdentifier("showHome", sender: self)
	}
	
}
