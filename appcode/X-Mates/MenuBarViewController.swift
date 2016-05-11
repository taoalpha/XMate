//
//  MenuBarViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 3/7/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit
import FBSDKCoreKit
import FBSDKLoginKit

class MenuBarViewController: UITableViewController {
	
	var appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
	
	private var menuList = ["User", "Home", "History", "Message", "Logout"]
	
	override func viewDidLoad() {
		
	}
	
	override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return self.menuList.count
	}
	
	override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		
		let cell = tableView.dequeueReusableCellWithIdentifier(menuList[indexPath.row], forIndexPath: indexPath)
		
		if indexPath.row == 0
		{
			cell.imageView?.image = self.appDelegate.picture
			cell.textLabel?.text = self.appDelegate.xmate.user["username"] as? String
		}
		else
		{
			cell.textLabel?.text = menuList[indexPath.row]
		}
		
		return cell
	}
	
	override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
		
		if indexPath.row == 4
		{
			let alertController = UIAlertController(title: "Logout", message: nil, preferredStyle: UIAlertControllerStyle.Alert)
			
			let done = UIAlertAction(title: "OK", style: UIAlertActionStyle.Default, handler: {(action) -> Void in
				let loginManager = FBSDKLoginManager()
				loginManager.logOut()
				let next = self.storyboard!.instantiateViewControllerWithIdentifier("Login")
				self.presentViewController(next, animated: true, completion: nil)
			})
			let cancel = UIAlertAction(title: "Cancel", style: UIAlertActionStyle.Cancel, handler: nil)
			
			alertController.addAction(done)
			alertController.addAction(cancel)
			self.presentViewController(alertController, animated: true, completion: nil)
		}
	}
}
