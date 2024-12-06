import * as graphql from "@nestjs/graphql";
import { GameResolverBase } from "./base/game.resolver.base";
import { Game } from "./base/Game";
import { GameService } from "./game.service";

@graphql.Resolver(() => Game)
export class GameResolver extends GameResolverBase {
  constructor(protected readonly service: GameService) {
    super(service);
  }
}
