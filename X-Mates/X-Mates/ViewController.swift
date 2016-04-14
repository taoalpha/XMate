//
//  ViewController.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 3/5/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit
import FBSDKCoreKit
import FBSDKLoginKit

class ViewController: UIViewController, FBSDKLoginButtonDelegate {
	
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var pageController: UIPageControl!
	
	var appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
	let swipeGestureLeft = UISwipeGestureRecognizer()
	let swipeGestureRight = UISwipeGestureRecognizer()
	let loginButton = FBSDKLoginButton()
	
	let messageList = ["Find Your Exercise Group\n\n Have a more enjoyable and more persistent\n work out with friends",
		"Make Friends While Exercising\n\n Let chemistry really work. Get the social\n motivation you need to succeed",
		"Monitor Your Exercise\n\n Match you with a mate with common\n interest and similar work out intensity level"]
	
	override func viewDidAppear(animated: Bool) {
		super.viewDidAppear(animated)
		
		if FBSDKAccessToken.currentAccessToken() != nil
		{
			// User is already logged in, do work such as go to next view controller.
			print("User is already logged in!")
			self.getFacebookUserData()
			let next = self.storyboard!.instantiateViewControllerWithIdentifier("Reveal")
			self.presentViewController(next, animated: true, completion: nil)
		}
		else
		{
			loginButton.readPermissions = ["public_profile", "email"]
			loginButton.delegate = self
			loginButton.center = CGPoint(x: 187.5, y: 550)
			self.view.addSubview(loginButton)
		}
	}
	
	override func viewDidLoad() {
		super.viewDidLoad()
		self.configureGesture()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
		// Dispose of any resources that can be recreated.
	}

	func loginButton(loginButton: FBSDKLoginButton!, didCompleteWithResult result: FBSDKLoginManagerLoginResult!, error: NSError!) {
		if error == nil
		{
			print("Login Complete!")
			self.getFacebookUserData()
			self.performSegueWithIdentifier("setUpProfile", sender: self)
		}
		else
		{
			print(error.localizedDescription)
		}
	}
	
	func loginButtonDidLogOut(loginButton: FBSDKLoginButton!) {
		print("User logged out!")
	}
	
	func configureGesture() {
		// set gesture direction
		self.swipeGestureLeft.direction = UISwipeGestureRecognizerDirection.Left
		self.swipeGestureRight.direction = UISwipeGestureRecognizerDirection.Right
		
		// add gesture target
		self.swipeGestureLeft.addTarget(self, action: "handleSwipeLeft:")
		self.swipeGestureRight.addTarget(self, action: "handleSwipeRight:")
		
		// add gesture in to view
		self.view.addGestureRecognizer(self.swipeGestureLeft)
		self.view.addGestureRecognizer(self.swipeGestureRight)
		
		self.setCurrentMessageLabel()
	}
	
	// increase page number on swift left
	func handleSwipeLeft(gesture: UISwipeGestureRecognizer){
		if self.pageController.currentPage < 2
		{
			self.pageController.currentPage += 1
			self.setCurrentMessageLabel()
		}
	}
	
	// reduce page number on swift right
	func handleSwipeRight(gesture: UISwipeGestureRecognizer){
		if self.pageController.currentPage != 0
		{
			self.pageController.currentPage -= 1
			self.setCurrentMessageLabel()
		}
	}
	
	// set current message label
	private func setCurrentMessageLabel() {
		self.messageLabel.text = self.messageList[self.pageController.currentPage]
	}
	
	private func getFacebookUserData() {
		
		let params = ["fields" : "id, name, email, first_name, last_name, gender, picture"]
		let request = FBSDKGraphRequest(graphPath: "me", parameters: params, HTTPMethod: "GET")
		
		request.startWithCompletionHandler({ (connection, result, error) -> Void in
			if error != nil
			{
				print("Error: \(error)")
			}
			else
			{
				print("fetched user: \(result)")
				
				self.appDelegate.xmate.user["_id"] = result.valueForKey("id") as? String
				self.appDelegate.xmate.user["username"] = result.valueForKey("name") as? String
				self.appDelegate.xmate.user["email"] = result.valueForKey("email") as? String
				self.appDelegate.xmate.user["first_name"] = result.valueForKey("first_name") as? String
				self.appDelegate.xmate.user["last_name"] = result.valueForKey("last_name") as? String
				
				var gender = result.valueForKey("gender") as? String
				if gender == "male"
				{
					gender = "Male"
				}
				else if gender == "female"
				{
					gender = "Female"
				}
				else
				{
					gender = ""
				}
				self.appDelegate.xmate.user["gender"] = gender
				
				let picURL = result.valueForKey("picture")?.valueForKey("data")?.valueForKey("url") as! String
				self.appDelegate.picture = UIImage(data: NSData(contentsOfURL: NSURL(string: picURL)!)!)!
			}
		})
	}
	
}

