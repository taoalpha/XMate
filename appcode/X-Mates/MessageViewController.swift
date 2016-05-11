//
//  MessageViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 4/14/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit

class MessageViewController: UITableViewController {

	@IBOutlet weak var openMenuBar: UIBarButtonItem!
	
	private let messageURL = "http://192.168.99.100:4000/message/"
	private let userURL = "http://192.168.99.100:4000/user/"
	private let scheduleURL = "http://192.168.99.100:4000/schedule/"
	
	private var appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
	private var messageList = [NSDictionary]()
	
	override func viewDidAppear(animated: Bool) {
		super.viewDidAppear(animated)
	}
	
	override func viewDidLoad() {
		openMenuBar.target = self.revealViewController()
		openMenuBar.action = #selector(SWRevealViewController.revealToggle(_:))
		
		self.view.addGestureRecognizer(self.revealViewController().panGestureRecognizer())
		
		self.appDelegate.xmate.get(self.userURL, mode: "user")
		self.getMessages()
		self.tableView.reloadData()
	}
	
	override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
		
		if self.messageList.count == 0
		{
			let defaultMsg = UILabel()
			defaultMsg.textAlignment = NSTextAlignment.Center
			defaultMsg.textColor = UIColor.lightGrayColor()
			defaultMsg.text = "No Message"
			tableView.separatorStyle = UITableViewCellSeparatorStyle.None
			tableView.backgroundView = defaultMsg
			return 0
		}
		else{
			tableView.backgroundView = nil
			return 1
		}
	}
	
	override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return self.messageList.count
	}
	
	override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
		let cell = tableView.dequeueReusableCellWithIdentifier("messageCell", forIndexPath: indexPath)
		
//		if self.messageList.count != 0
//		{
		if (self.messageList[indexPath.row]["type"] as! String) == "plaintext"
		{
			cell.textLabel?.text = String(indexPath.row + 1) + ". Decline Message"
		}
		else
		{
			let content = self.messageList[indexPath.row]["content"] as! String
			cell.textLabel?.text = String(indexPath.row + 1) + ". " + content
		}
//		}
		
		return cell
	}
	
	override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
		
		let formatter = NSDateFormatter()
		formatter.dateFormat = "MMM-dd-YYYY hh:mm a"
		
		let postID = self.messageList[indexPath.row]["post_id"] as! String
		
		self.appDelegate.xmate.get(self.scheduleURL, mode: "schedule", id: postID)
		
		let user = "User: " + (self.appDelegate.xmate.schedule["owner"] as! String)
		let st = self.appDelegate.xmate.schedule["start_time"] as! NSTimeInterval
		let nsdate = NSDate(timeIntervalSince1970: st)
		let time = "Time: " + formatter.stringFromDate(nsdate)
		let category = "Category: " + (self.appDelegate.xmate.schedule["type"] as! String)
		
		let msg = user + "\n" + time + "\n" + category
		
		let alertController = UIAlertController(title: "Details", message: msg, preferredStyle: UIAlertControllerStyle.Alert)
		
		let ok = UIAlertAction(title: "Ok", style: UIAlertActionStyle.Default, handler: nil)
		
		alertController.addAction(ok)
		self.presentViewController(alertController, animated: true, completion: nil)

	}
	
	override func tableView(tableView: UITableView, canEditRowAtIndexPath indexPath: NSIndexPath) -> Bool {
		return true
	}
	
	override func tableView(tableView: UITableView, editActionsForRowAtIndexPath indexPath: NSIndexPath) -> [UITableViewRowAction]? {
		let message = self.messageList[indexPath.row]
		
		if (message["type"] as! String) == "plaintext"
		{
			let read = UITableViewRowAction(style: .Normal, title: "Read") { action in
				self.appDelegate.xmate.put(self.messageURL, mode: "read", mid: message["_id"] as! String)
				self.getMessages()
				tableView.reloadData()
			}
			
			return [read]
		}
		else
		{
			let accept = UITableViewRowAction(style: .Normal, title: "Accept") { action in
				self.appDelegate.xmate.put(self.messageURL, mode: "accept", mid: message["_id"] as! String)
				self.getMessages()
				tableView.reloadData()
			}
			let decline = UITableViewRowAction(style: .Default, title: "Decline") { action in
				self.appDelegate.xmate.put(self.messageURL, mode: "decline", mid: message["_id"] as! String)
				self.getMessages()
				tableView.reloadData()
			}
			
			return [accept, decline]
		}
		
	}
	
	func getMessages() {
		self.messageList.removeAll()
		let list = self.appDelegate.xmate.user["unprocessed_message"] as! [String]
		if list.count != 0
		{
			for index in 0...list.count-1
			{
				let sid = list[index]
				self.appDelegate.xmate.get(self.messageURL, mode: "message", id: sid)
				self.messageList.append(self.appDelegate.xmate.message)
			}
		}
	}
}
