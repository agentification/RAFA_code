

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a d)
(on b i)
(on c b)
(on d h)
(on e g)
(ontable f)
(ontable g)
(on h e)
(ontable i)
(clear a)
(clear c)
(clear f)
)
(:goal
(and
(on b f)
(on c h)
(on d a)
(on f d)
(on g i)
(on h b)
(on i e))
)
)


