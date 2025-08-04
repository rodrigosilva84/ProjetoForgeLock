#!/usr/bin/env python
"""
Management command para verificar e atualizar status das assinaturas
Executa verificações automáticas de assinaturas expiradas e período de carência
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Subscription, User
from django.db import transaction
from core.notifications import notification_service


class Command(BaseCommand):
    help = 'Verifica e atualiza status das assinaturas automaticamente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executa sem fazer alterações no banco',
        )
        parser.add_argument(
            '--send-notifications',
            action='store_true',
            help='Envia notificações para usuários',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        send_notifications = options['send_notifications']
        
        self.stdout.write(
            self.style.SUCCESS('🔍 Iniciando verificação de assinaturas...')
        )
        
        # Estatísticas
        stats = {
            'expired': 0,
            'grace_period_started': 0,
            'grace_period_ended': 0,
            'notifications_sent': 0,
        }
        
        # 1. Verificar assinaturas que expiraram hoje
        self.stdout.write('\n📅 Verificando assinaturas expiradas...')
        expired_subscriptions = Subscription.objects.filter(
            status__in=['active', 'trial'],
            end_date__lte=timezone.now()
        )
        
        for subscription in expired_subscriptions:
            if not dry_run:
                with transaction.atomic():
                    subscription.status = 'grace_period'
                    subscription.grace_period_until = timezone.now() + timedelta(days=15)
                    subscription.save()
                    
                    self.stdout.write(
                        f'   ⚠️  Assinatura expirada: {subscription.user.email} '
                        f'(Plano: {subscription.plan.name})'
                    )
                    stats['expired'] += 1
            else:
                self.stdout.write(
                    f'   ⚠️  [DRY-RUN] Assinatura expiraria: {subscription.user.email} '
                    f'(Plano: {subscription.plan.name})'
                )
        
        # 2. Verificar período de carência que acabou
        self.stdout.write('\n⏰ Verificando período de carência...')
        grace_period_ended = Subscription.objects.filter(
            status='grace_period',
            grace_period_until__lte=timezone.now()
        )
        
        for subscription in grace_period_ended:
            if not dry_run:
                with transaction.atomic():
                    subscription.status = 'expired'
                    subscription.save()
                    
                    self.stdout.write(
                        f'   ❌ Carência encerrada: {subscription.user.email} '
                        f'(Plano: {subscription.plan.name})'
                    )
                    stats['grace_period_ended'] += 1
            else:
                self.stdout.write(
                    f'   ❌ [DRY-RUN] Carência encerraria: {subscription.user.email} '
                    f'(Plano: {subscription.plan.name})'
                )
        
        # 3. Verificar assinaturas que vencem em 10 dias
        self.stdout.write('\n📧 Verificando notificações...')
        if send_notifications:
            ten_days_from_now = timezone.now() + timedelta(days=10)
            expiring_soon = Subscription.objects.filter(
                status__in=['active', 'trial'],
                end_date__lte=ten_days_from_now,
                end_date__gt=timezone.now()
            )
            
            for subscription in expiring_soon:
                # Verificar se já enviou notificação recentemente (últimos 3 dias)
                if (not subscription.last_notification_sent or 
                    subscription.last_notification_sent < timezone.now() - timedelta(days=3)):
                    
                    if not dry_run:
                        with transaction.atomic():
                            subscription.last_notification_sent = timezone.now()
                            subscription.save()
                            
                            # Enviar notificação real
                            email_sent, sms_sent = notification_service.send_subscription_notification(
                                subscription, 'expiring_soon'
                            )
                            
                            self.stdout.write(
                                f'   📧 Notificação enviada: {subscription.user.email} '
                                f'(Vence em {subscription.get_days_remaining()} dias) '
                                f'[Email: {"✅" if email_sent else "❌"}, SMS: {"✅" if sms_sent else "❌"}]'
                            )
                            stats['notifications_sent'] += 1
                    else:
                        self.stdout.write(
                            f'   📧 [DRY-RUN] Notificação seria enviada: {subscription.user.email} '
                            f'(Vence em {subscription.get_days_remaining()} dias)'
                        )
        
        # 4. Resumo
        self.stdout.write('\n📊 Resumo da verificação:')
        self.stdout.write(f'   • Assinaturas expiradas: {stats["expired"]}')
        self.stdout.write(f'   • Carência encerrada: {stats["grace_period_ended"]}')
        self.stdout.write(f'   • Notificações enviadas: {stats["notifications_sent"]}')
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('\n⚠️  MODO DRY-RUN: Nenhuma alteração foi feita')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\n✅ Verificação concluída com sucesso!')
            )
        
        self.stdout.write('\n💡 Dicas:')
        self.stdout.write('   • Execute diariamente: python manage.py check_subscriptions')
        self.stdout.write('   • Teste primeiro: python manage.py check_subscriptions --dry-run')
        self.stdout.write('   • Com notificações: python manage.py check_subscriptions --send-notifications') 