//
//  TimelineCell.h
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import <UIKit/UIKit.h>


@interface TimelineCell : UITableViewCell {
	IBOutlet UILabel* username;
	IBOutlet UILabel* tweet;
	IBOutlet UILabel* date;
	IBOutlet UIImageView* profileImage;
	IBOutlet UIActivityIndicatorView* act;
	IBOutlet UIButton* likeButton;
	IBOutlet UIButton* dislikeButton;
}

@property (assign) IBOutlet UILabel* username;
@property (assign) IBOutlet UILabel* tweet;
@property (assign) IBOutlet UILabel* date;
@property (assign) IBOutlet UIImageView* profileImage;
@property (assign) IBOutlet UIActivityIndicatorView* act;
@property (assign) IBOutlet UIButton* likeButton;
@property (assign) IBOutlet UIButton* dislikeButton;



@end
