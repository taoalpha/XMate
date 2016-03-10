//
//  UserInfo.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 3/5/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit

public final class UserInfo: NSObject {
	
	public let id: String
	public let username: String
	public let avatar: String
	public let addr: String
	public let height: Int
	public let weight: Int
	public let age: Int
	public let gender: Int
	public let email: String
	public let prefer: String
	
	public init(id: String, username: String, avatar: String, addr: String, height: Int, weight: Int, age: Int, gender: Int, email: String, prefer: String) {
		self.id = id
		self.username = username
		self.avatar = avatar
		self.addr = addr
		self.height = height
		self.weight = weight
		self.age = age
		self.gender = gender
		self.email = email
		self.prefer = prefer
		
		super.init()
	}
}
