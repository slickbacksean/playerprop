import { Module } from "@nestjs/common";
import { PlayerModuleBase } from "./base/player.module.base";
import { PlayerService } from "./player.service";
import { PlayerController } from "./player.controller";
import { PlayerResolver } from "./player.resolver";

@Module({
  imports: [PlayerModuleBase],
  controllers: [PlayerController],
  providers: [PlayerService, PlayerResolver],
  exports: [PlayerService],
})
export class PlayerModule {}
