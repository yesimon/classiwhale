//
//  ClassiwhaleSingleton.m
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import "ClassiwhaleSingleton.h"

@implementation ClassiwhaleSingleton

static ClassiwhaleSingleton *sharedInstance = nil;

// Get the shared instance and create it if necessary.
+ (ClassiwhaleSingleton*)sharedInstance {
	if (sharedInstance == nil) {
		sharedInstance = [[super allocWithZone:NULL] init];
	}
	
	return sharedInstance;
}


// We don't want to allocate a new instance, so return the current one.
+ (id)allocWithZone:(NSZone*)zone {
	return [[self sharedInstance] retain];
}

// Equally, we don't want to generate multiple copies of the singleton.
- (id)copyWithZone:(NSZone *)zone {
	return self;
}

// Once again - do nothing, as we don't have a retain counter for this object.
- (id)retain {
	return self;
}

// Replace the retain counter so we can never release this object.
- (NSUInteger)retainCount {
	return NSUIntegerMax;
}

// This function is empty, as we don't want to let the user release this object.
- (void)release {
	
}

//Do nothing, other than return the shared instance - as this is expected from autorelease.
- (id)autorelease {
	return self;
}

@end
