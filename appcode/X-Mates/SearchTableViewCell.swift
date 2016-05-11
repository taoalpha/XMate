//
//  SearchTableViewCell.swift
//  X-Mates
//
//  Created by Jiangyu Mao on 5/8/16.
//  Copyright © 2016 CloudGroup. All rights reserved.
//

import UIKit

class SearchTableViewCell: UITableViewCell {
	
	@IBOutlet weak var userLabel: UILabel!
	@IBOutlet weak var startLabel: UILabel!
	@IBOutlet weak var joinButton: UIButton!

    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
