//
//  SearchViewController.h
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import <UIKit/UIKit.h>


@interface SearchViewController : UIViewController <UISearchDisplayDelegate, UITableViewDataSource, UITableViewDelegate> {
	NSMutableArray* _data;
}

- (void)searchClassiwhale:(NSString*)query;

@end
