//
//  ProfileViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 3/5/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit

class ProfileViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
	
	let tableData = ["Gender", "Birthdate", "Height", "Weight"]
	
	override func viewDidLoad() {
		super.viewDidLoad()
		// Do any additional setup after loading the view, typically from a nib.
		
	}
	
	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
		// Dispose of any resources that can be recreated.
	}
	
	func numberOfSectionsInTableView(tableView: UITableView) -> Int {
		return 1
	}
	
	func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return self.tableData.count
	}
	
	func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCellWithIdentifier("profileCell", forIndexPath: indexPath)
		
		cell.textLabel?.text = self.tableData[indexPath.row]
		
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
		let male = UIAlertAction(title: "Male", style: UIAlertActionStyle.Default, handler: {(action) -> Void in cell.detailTextLabel?.text = "Male"})
		let female = UIAlertAction(title: "Female", style: UIAlertActionStyle.Default, handler: {(action) -> Void in cell.detailTextLabel?.text = "Female"})
		
		alertController.addAction(male)
		alertController.addAction(female)
		
		self.presentViewController(alertController, animated: true, completion: nil)
	}
	
	func birthdatePicker(cell: UITableViewCell) {
		let alertController = UIAlertController(title: "\n\n\n\n\n\n\n\n\n", message: nil, preferredStyle: UIAlertControllerStyle.ActionSheet)
		let datePicker = UIDatePicker()
		datePicker.datePickerMode = UIDatePickerMode.Date
		datePicker.date = NSDate()
		let formatter = NSDateFormatter()
		formatter.dateStyle = .MediumStyle
		let done = UIAlertAction(title: "Done", style: UIAlertActionStyle.Default, handler: {(action) -> Void in cell.detailTextLabel?.text = formatter.stringFromDate(datePicker.date)})
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
		self.performSegueWithIdentifier("showHome", sender: self)
	}
	
}
