//
//  TwitterUserCell.h
//  classiwhale
//
//  Created by Alex Churchill on 3/15/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>


@interface TwitterUserCell : UITableViewCell {
  IBOutlet UILabel *user_name;
  IBOutlet UILabel *screen_name;
	IBOutlet UIImageView* profileImage;
	IBOutlet UIActivityIndicatorView* act;
}

@property (nonatomic, retain) IBOutlet UILabel *user_name;
@property (nonatomic, retain) IBOutlet UILabel *screen_name;
@property (assign) IBOutlet UIImageView* profileImage;
@property (assign) IBOutlet UIActivityIndicatorView* act;

@end
