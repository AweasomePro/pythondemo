from account.models import User
from account.invitation.models import InviteRecord
from common.exceptions import ConditionDenied


def invited_service(inviter_phone_number,invitee):
    try:
        inviter_user = User.objects.get(phone_number=inviter_phone_number)
        InviteRecord.objects.create(inviter = inviter_user,invitee=invitee)
    except User.DoesNotExist:
        raise ConditionDenied(detail='不存在该邀请人')


def promotion_service(pointpay):
    #充值用户
    user = pointpay.user

    # == 活动1 首次充值，赠送 20%积分
    if pointpay.is_first_recharge():
        from account.models import BillHistory
        BillHistory.createForFirstRechargeGift(pointpay)
    # == 活动2  邀请充值送 积分
    #判断是否在被邀请名单并且未充值过
    try:
        inviteRecord = InviteRecord.objects.get(invitee=user,recharged=False)
        inviter = inviteRecord.inviter
        # 获得用户充值的积分，及邀请者将要获得的积分，并且保存至
        pay_points = pointpay.number
        InviteRecord.handle_new_invitee_recharge(inviteRecord,pointpay)
    except InviteRecord.DoesNotExist:
        #不是活动用户 或者已经奖励过了 直接pass
        pass