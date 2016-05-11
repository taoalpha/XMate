//
//  XMateManager.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 4/14/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit

class XMateManager: NSObject {
	
	private let userURL = "http://192.168.99.100:4000/user/"
	
	var user : NSMutableDictionary
	var schedule : NSMutableDictionary
	var matches : [NSDictionary]
	var message : NSDictionary
	
	override init() {
		self.user = NSMutableDictionary()
		self.schedule = NSMutableDictionary()
		self.matches = [NSDictionary]()
		self.message = NSDictionary()
	}
	
	func post(url: String, mode: String) {
		if mode == "user"
		{
			let data = NSDictionary(dictionary: self.user)
			let res = Just.post(url, data: data as! [String : AnyObject]).json
			self.user = NSMutableDictionary(dictionary: res as! NSDictionary)
		}
		else if mode == "schedule"
		{
			
			let data = NSDictionary(dictionary: self.schedule)
			let res = Just.post(url, data: data as! [String : AnyObject]).json
			self.schedule = NSMutableDictionary(dictionary: res as! NSDictionary)
		}
		
		self.get(self.userURL, mode: "user")
	}
	
	func post(url: String, mode: String, id: String) {
		if mode == "invite"
		{
			let data = ["sender_id":self.user["_id"]!, "receiver_id":id, "post_id": self.schedule["_id"]!, "type":"invite"]
			let res = Just.post(url, data: data).json
			print("The invite id is \(res)")
		}
		else if mode == "join"
		{
			let data = ["sender_id":self.user["_id"]!, "receiver_id":id, "post_id": self.schedule["_id"]!, "type":"join"]
			let res = Just.post(url, data: data).json
			print("The join id is \(res)")
		}
		
		self.get(self.userURL, mode: "user")
	}
	
	func put(url: String, mode: String, mid: String) {
		if mode == "accept"
		{
			let data = ["sender_id":self.user["_id"]!, "_id":mid, "type":"accept"]
			let res = Just.put(url, data: data).json
			print("The accept id is \(res)")
		}
		else if mode == "decline"
		{
			let data = ["sender_id":self.user["_id"]!, "_id":mid, "type":"decline"]
			let res = Just.put(url, data: data).json
			print("The decline id is \(res)")
		}
		
		self.get(self.userURL, mode: "user")
	}
	
	func get(url: String, mode: String) -> String {
		let res = Just.get(url + (self.user["_id"] as! String)).json
		print(res)
		if res === nil
		{
			return "Server Error"
		}
		else if res!["status"] !== nil
		{
			return "No Match"
		}
		else
		{
			self.user = NSMutableDictionary(dictionary: res as! NSDictionary)
			return "Ok"
		}
	}
	
	func get(url: String, mode: String, id: String) {
		
		if mode == "schedule"
		{
			let res = Just.get(url + id).json
			self.schedule = NSMutableDictionary(dictionary: res as! NSDictionary)
		}
		else if mode == "message"
		{
			let res = Just.get(url + id).json
			self.message = res as! NSDictionary
		}
		
	}
	
	func search(url: String, data: [String: AnyObject]) -> String {
		let res = Just.post(url, data: data).json
		print(res)
		if res === nil
		{
			return "Server Error"
		}
		else
		{
			self.matches = res as! [NSDictionary]
			return "Ok"
		}
	}
}
