//
//  GetGUIDState.h
//  TaskCoach
//
//  Created by Jérôme Laheurte on 29/01/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "BaseState.h"

@interface GetGUIDState : BaseState <State>
{
	NSInteger state;
}

@end