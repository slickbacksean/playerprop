import * as graphql from "@nestjs/graphql";
import { PlayerResolverBase } from "./base/player.resolver.base";
import { Player } from "./base/Player";
import { PlayerService } from "./player.service";

@graphql.Resolver(() => Player)
export class PlayerResolver extends PlayerResolverBase {
  constructor(protected readonly service: PlayerService) {
    super(service);
  }
}
