//
//  SearchViewController.h
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import <UIKit/UIKit.h>


@interface SearchViewController : UIViewController <UISearchBarDelegate, UISearchDisplayDelegate, UITableViewDataSource, UITableViewDelegate> {
	NSMutableArray* _data;
	IBOutlet UILabel* grayLabel;
}

@property (nonatomic, retain) IBOutlet UILabel* grayLabel;

- (void)searchClassiwhale:(NSString*)query;

@end
