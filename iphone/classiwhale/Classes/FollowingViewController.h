//
//  FollowingViewController.h
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import <UIKit/UIKit.h>


@interface FollowingViewController : UIViewController <UITableViewDelegate, UITableViewDataSource> {
	IBOutlet UITableView *table;
	NSArray* users;
}

@property (nonatomic, retain) IBOutlet UITableView *table;

@end
