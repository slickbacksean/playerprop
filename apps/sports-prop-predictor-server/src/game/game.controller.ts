import * as common from "@nestjs/common";
import * as swagger from "@nestjs/swagger";
import { GameService } from "./game.service";
import { GameControllerBase } from "./base/game.controller.base";

@swagger.ApiTags("games")
@common.Controller("games")
export class GameController extends GameControllerBase {
  constructor(protected readonly service: GameService) {
    super(service);
  }
}
