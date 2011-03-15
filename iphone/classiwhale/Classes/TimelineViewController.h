//
//  TimelineViewController.h
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import <UIKit/UIKit.h>


@interface TimelineViewController : UIViewController <UITableViewDelegate, UITableViewDataSource> {
	IBOutlet UITableView *table;
	NSArray* timeline;
	IBOutlet UISegmentedControl* segmentedControl;
}

@property (nonatomic, retain) IBOutlet UITableView *table;
@property (nonatomic, retain) IBOutlet UISegmentedControl* segmentedControl;


- (void) gotTwitterPic:(NSNotification *)info;
- (IBAction) segmentSwitched;
- (IBAction) likeClicked:(id)sender;
- (IBAction) dislikeClicked:(id)sender;
- (void) submitRating:(Boolean)rating tweetID:(NSString*)tweetID;

@end
