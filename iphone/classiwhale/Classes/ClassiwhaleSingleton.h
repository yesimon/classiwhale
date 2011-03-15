//
//  ClassiwhaleSingleton.h
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "SA_OAuthTwitterEngine.h" 
#import "SA_OAuthTwitterController.h"



@interface ClassiwhaleSingleton : NSObject <SA_OAuthTwitterControllerDelegate> {
	SA_OAuthTwitterEngine *twitterEngine;


}

+ (ClassiwhaleSingleton*)sharedInstance;
- (void) loginToTwitter:(UIViewController*)vc;

@end
