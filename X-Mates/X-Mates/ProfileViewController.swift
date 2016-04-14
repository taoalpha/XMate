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

class ProfileViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
	
	@IBOutlet weak var firstName: UITextField!
	@IBOutlet weak var lastName: UITextField!
	@IBOutlet weak var email: UITextField!
	
	private let SUCCESSE_STATUS = "1"
	private let userURL = "http://192.168.99.100:2000/user/"
	private let tableData = ["Gender", "Birthdate", "Height", "Weight"]
	
	private var appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
	private var gender = ""
	private var birthday = ""
	private var height = ""
	private var weight = ""
		
	override func viewDidLoad() {
		super.viewDidLoad()
		// Do any additional setup after loading the view, typically from a nib.
		
//		self.appDelegate.xmate.post(userURL, mode: "user")

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
		//TODO: need to find a better way to do this
		
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
		//tableView.deselectRowAtIndexPath(indexPath, animated: true)
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
	
	func heightPicker(cell: UITableViewCell) {
		//TODO:
	}
	
	func weightPicker(cell: UITableViewCell) {
		//TODO:
	}
	
	@IBAction func goToHome(sender: UIBarButtonItem) {
		self.appDelegate.xmate.user["first_name"] = firstName.text
		self.appDelegate.xmate.user["last_name"] = lastName.text
		self.appDelegate.xmate.user["email"] = email.text
		
		self.appDelegate.xmate.user["gender"] = self.gender
		self.appDelegate.xmate.user["birthday"] = self.birthday
		self.appDelegate.xmate.user["height"] = self.height
		self.appDelegate.xmate.user["weight"] = self.weight
		
		self.performSegueWithIdentifier("showHome", sender: self)
	}
	
}
