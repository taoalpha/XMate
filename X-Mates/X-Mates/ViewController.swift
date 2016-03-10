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
	
	let swipeGestureLeft = UISwipeGestureRecognizer()
	let swipeGestureRight = UISwipeGestureRecognizer()
	
	let loginButton = FBSDKLoginButton()
	
	let messageList = ["Find Your Exercise Group\n\n Have a more enjoyable and more persistent\n work out with friends",
		"Make Friends While Exercising\n\n Let chemistry really work. Get the social\n motivation you need to succeed",
		"Monitor Your Exercise\n\n Match you with a mate with common\n interest and similar work out intensity level"]

	override func viewDidLoad() {
		super.viewDidLoad()
		
		if (FBSDKAccessToken.currentAccessToken() != nil)
		{
			// User is already logged in, do work such as go to next view controller.
			print("User is already logged in!")
			loginButton.readPermissions = ["public_profile", "email"]
			loginButton.delegate = self
			loginButton.center = CGPoint(x: 187.5, y: 550)
			self.view.addSubview(loginButton)
		}
		else
		{
			loginButton.readPermissions = ["public_profile", "email"]
			loginButton.delegate = self
			loginButton.center = CGPoint(x: 187.5, y: 550)
			self.view.addSubview(loginButton)
		}
		
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
	
}

