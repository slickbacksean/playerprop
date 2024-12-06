import { Injectable } from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { PlayerServiceBase } from "./base/player.service.base";

@Injectable()
export class PlayerService extends PlayerServiceBase {
  constructor(protected readonly prisma: PrismaService) {
    super(prisma);
  }
}
