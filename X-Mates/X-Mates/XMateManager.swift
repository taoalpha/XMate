//
//  XMateManager.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 4/14/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit

class XMateManager: NSObject {
	
	var user : NSMutableDictionary
	var schedule : NSMutableDictionary
	
	override init() {
		self.user = NSMutableDictionary()
		self.schedule = NSMutableDictionary()
	}
	
	func post(url: String, mode: String) {
		
		if mode == "user"
		{
			let data = NSDictionary(dictionary: self.user)
			let res = Just.post(url, data: data as! [String : AnyObject]).json
			print(res)
			//self.user = NSMutableDictionary(dictionary: res as! NSDictionary)
		}
		else if mode == "schedule"
		{
			
			let data = NSDictionary(dictionary: self.schedule)
			let res = Just.post(url, data: data as! [String : AnyObject]).json
			print(res)
			//self.schedule = NSMutableDictionary(dictionary: res as! NSDictionary)
		}
		
	}
	
	func get(url: String, mode: String) {
		
		if mode == "user"
		{
			let res = Just.get(url + (self.user["_id"] as! String)).json
			print(res)
			self.user = NSMutableDictionary(dictionary: res as! NSDictionary)
		}
		else if mode == "schedule"
		{
			let res = Just.get(url + (self.schedule["_id"] as! String))
			self.schedule = NSMutableDictionary(dictionary: res.json as! NSDictionary)
		}
	}
}
